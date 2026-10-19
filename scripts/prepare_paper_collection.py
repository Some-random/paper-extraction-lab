#!/usr/bin/env python3
"""Freeze private native-source locators and existing-fulltext identifiers.

Reads only explicitly supplied roots. Source papers are never copied. A bounded
JATS header check identifies reusable native inputs; the processing worker must
validate the complete XML before retaining extracted content.
"""
import argparse
import csv
import hashlib
import json
import re
import time
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OWN_ROOTS = [
    "experiments/pmc_cns_biology_2026-10-14",
    "experiments/pmc_native_500_2026-10-15",
    "experiments/pmc_native_v4_citations_2026-10-15",
    "experiments/pmc_native_fresh_500_2026-10-15",
    "experiments/corpus_count_2026-10-17/pmc_expansion",
]


class AbstractOnlyArticle(ValueError):
    """A complete XML article with no fulltext body is not existing fulltext."""


def normalize_pmcid(value):
    match = re.fullmatch(r"(?:PMC)?0*([1-9][0-9]*)(?:\.[0-9]+)?", str(value).strip(), re.I)
    return "PMC" + match.group(1) if match else ""


def normalize_pmid(value):
    text = str(value or "").strip()
    return str(int(text)) if re.fullmatch(r"[0-9]+", text) and int(text) > 0 else ""


def normalize_doi(value):
    text = re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", str(value or "").strip(), flags=re.I)
    return text.casefold() if re.match(r"^10\.[0-9]{4,9}/\S+$", text) else ""


def inferred_pmcid(path):
    for value in (path.stem, path.parent.name):
        pmcid = normalize_pmcid(value)
        if pmcid:
            return pmcid
    return ""


def contained(path, roots):
    """Resolving both the file and roots rejects symlink escapes."""
    resolved = path.resolve(strict=True)
    return any(resolved.is_relative_to(root) for root in roots)


def article_header(path, maximum_bytes=1024 * 1024):
    """Read bounded metadata through a JATS body start, without XML entities."""
    parser = ET.XMLPullParser(events=("start", "end"))
    ids = {}
    scanned = 0
    saw_article = False
    saw_meta = False
    saw_body = False
    in_meta = 0
    declaration_tail = b""
    reached_eof = False
    with path.open("rb") as handle:
        while scanned < maximum_bytes:
            data = handle.read(min(32768, maximum_bytes - scanned))
            if not data:
                parser.close()
                reached_eof = True
                break
            scanned += len(data)
            # External entities are not resolved by ElementTree. Reject entity
            # declarations as well so this inventory cannot expand internal ones.
            if b"<!ENTITY" in (declaration_tail + data).upper():
                raise ValueError("entity_declaration")
            declaration_tail = data[-16:]
            parser.feed(data)
            for event, element in parser.read_events():
                tag = element.tag.rsplit("}", 1)[-1]
                if event == "start":
                    if not saw_article:
                        if tag != "article":
                            raise ValueError("not_jats_article")
                        saw_article = True
                    if tag == "article-meta":
                        in_meta += 1
                    if tag == "body":
                        saw_body = True
                elif tag == "article-id" and in_meta:
                    kind = element.attrib.get("pub-id-type", "").casefold()
                    ids.setdefault(kind, "".join(element.itertext()).strip())
                elif tag == "article-meta":
                    in_meta -= 1
                    saw_meta = True
            if saw_meta and saw_body:
                break
    if reached_eof and saw_article and not saw_body:
        raise AbstractOnlyArticle("valid_article_without_fulltext_body")
    if not (saw_article and saw_meta and saw_body):
        raise ValueError("missing_article_metadata_or_body_within_bound")
    pmcid = next((normalize_pmcid(ids[key]) for key in ("pmcid", "pmc", "pmcaid", "pmcaiid") if normalize_pmcid(ids.get(key, ""))), "")
    return {"pmcid": pmcid, "pmid": normalize_pmid(ids.get("pmid")),
            "doi": normalize_doi(ids.get("doi")), "metadata_bytes_scanned": scanned,
            "validation": "bounded_jats_metadata_and_body_start",
            "full_xml_validation": "deferred_to_processing"}


def prepare(output, manifest, allowed_roots, own_roots, old_fulltext_index=None,
            maximum_metadata_bytes=1024 * 1024):
    started = time.monotonic()
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    targets = [output / name for name in ("source_catalog.json", "presence_ids.csv", "preparation_summary.json")]
    if any(path.exists() for path in targets):
        raise FileExistsError("Frozen preparation already exists; use it rather than overwriting it")
    roots = [Path(path).resolve(strict=True) for path in allowed_roots if Path(path).is_dir()]
    own_roots = [Path(path).absolute() for path in own_roots]
    roots.extend(path.resolve(strict=True) for path in own_roots if path.is_dir())
    roots = list(dict.fromkeys(roots))
    candidates = {}
    missing_roots = [str(path) for path in own_roots if not path.is_dir()]
    if manifest:
        with Path(manifest).open(newline="") as handle:
            for row in csv.DictReader(handle):
                path = Path(row["source_path"]).absolute()
                candidates.setdefault(str(path), (path, normalize_pmcid(row.get("pmcid", "")), "shared_xml_manifest"))
    for own_root in own_roots:
        if not own_root.is_dir():
            continue
        # Only native source names; versions.xml and metadata responses are not
        # articles. pathlib does not recursively traverse symlink directories.
        for path in own_root.rglob("source.xml"):
            candidates.setdefault(str(path), (path, inferred_pmcid(path), "own_native_cache"))
    counters = Counter()
    failures = []
    native = []
    presence = set()
    physical_bytes = {}
    for index, (path, expected, origin) in enumerate(sorted(candidates.values(), key=lambda item: str(item[0]))):
        try:
            if not contained(path, roots):
                counters["outside_explicit_roots"] += 1
                failures.append({"path": str(path), "pmcid": expected, "reason": "outside_explicit_roots"})
                continue
            stat = path.stat()
            if not path.is_file() or not stat.st_size:
                raise ValueError("empty_or_not_regular_file")
            # A source already present is excluded from acquisition even when
            # its XML is broken. Metadata selection without a file is excluded.
            if expected:
                presence.add((expected, "", "", str(path)))
            counters["existing_native_paths"] += 1
            metadata = article_header(path, maximum_metadata_bytes)
            actual = metadata["pmcid"] or expected
            if actual:
                presence.add((actual, metadata["pmid"], metadata["doi"], str(path)))
            if not actual:
                raise ValueError("no_pmcid")
            if expected and metadata["pmcid"] and expected != metadata["pmcid"]:
                raise ValueError("pmcid_mismatch")
            item = {"kind": "native_xml", "pmcid": actual, "path": str(path),
                    "bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns,
                    "origin": origin, **metadata}
            item["pmcid"] = actual
            native.append(item)
            physical_bytes[str(path.resolve())] = stat.st_size
            counters["catalog_native_variants"] += 1
        except AbstractOnlyArticle:
            presence.discard((expected, "", "", str(path)))
            counters["abstract_only_native_paths_excluded"] += 1
            failures.append({"path": str(path), "pmcid": expected, "reason": "abstract_only_xml"})
        except (OSError, ValueError, ET.ParseError) as error:
            # For malformed but existing XML, keep the inferred PMC identifier.
            if expected and path.is_file() and contained(path, roots):
                presence.add((expected, "", "", str(path)))
            counters["unusable_native_paths"] += 1
            failures.append({"path": str(path), "pmcid": expected,
                             "reason": type(error).__name__ + ": " + str(error)[:200]})
        if (index + 1) % 1000 == 0:
            print(json.dumps({"stage": "index_native_xml", "checked": index + 1,
                              "candidates": len(candidates), "catalog": len(native)}), flush=True)
    old_source = "old_section_text_index"
    if old_fulltext_index:
        with Path(old_fulltext_index).open(newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("has_sections") != "1":
                    counters["abstract_only_index_rows_excluded"] += 1
                    continue
                pmcid = normalize_pmcid(row.get("pmcid", ""))
                pmid = normalize_pmid(row.get("pmid", ""))
                if pmcid or pmid:
                    presence.add((pmcid, pmid, normalize_doi(row.get("doi", "")), old_source))
                    counters["old_section_text_index_rows"] += 1
    native.sort(key=lambda item: (item["pmcid"], item["path"]))
    targets[0].write_text(json.dumps(native, indent=2, ensure_ascii=False) + "\n")
    with targets[1].open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["pmcid", "pmid", "doi", "source"])
        writer.writerows(sorted(presence))
    summary = {
        "scope": "Known explicitly allowlisted fulltext locations; no cluster-wide absence claim",
        "complete": True, "counters": dict(counters), "native_candidates": len(candidates),
        "native_catalog_variants": len(native),
        "native_catalog_unique_pmcids": len({item["pmcid"] for item in native}),
        "native_catalog_variant_bytes": sum(item["bytes"] for item in native),
        "native_catalog_unique_resolved_bytes": sum(physical_bytes.values()),
        "presence_rows": len(presence),
        "presence_unique_pmcids": len({row[0] for row in presence if row[0]}),
        "presence_unique_pmids": len({row[1] for row in presence if row[1]}),
        "presence_unique_dois": len({row[2] for row in presence if row[2]}),
        "elapsed_seconds": time.monotonic() - started,
        "missing_own_roots": missing_roots, "allowed_roots": [str(path) for path in roots],
        "maximum_metadata_bytes_per_xml": maximum_metadata_bytes,
        "full_xml_integrity": "Deferred to processing; header checks are not full-file validation",
        "native_failures": failures,
        "frozen_inputs": {path.name: {"bytes": path.stat().st_size,
                           "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in targets[:2]},
    }
    targets[2].write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--xml-manifest", type=Path)
    parser.add_argument("--allowed-root", type=Path, action="append", default=[])
    parser.add_argument("--own-root", type=Path, action="append")
    parser.add_argument("--old-fulltext-index", type=Path)
    parser.add_argument("--maximum-metadata-bytes", type=int, default=1024 * 1024)
    args = parser.parse_args()
    roots = args.own_root if args.own_root is not None else [ROOT / path for path in DEFAULT_OWN_ROOTS]
    summary = prepare(args.output, args.xml_manifest, args.allowed_root, roots,
                      args.old_fulltext_index, args.maximum_metadata_bytes)
    print(json.dumps({key: summary[key] for key in ("native_catalog_variants", "native_catalog_unique_pmcids",
                       "presence_unique_pmcids", "presence_unique_pmids", "elapsed_seconds")}), flush=True)


if __name__ == "__main__":
    main()
