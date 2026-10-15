"""Serial, bounded biology acquisition retaining source figures; CPU only.

Uses the existing PMC downloader and native parser. No OCR, teacher inference,
recaptioning, panel segmentation, supplementary-file downloads or model training.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import os
import re
import shutil
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from urllib.error import URLError
from urllib.parse import parse_qs, unquote, urlsplit

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
from tokenizers import Tokenizer

from native_training import parse_jats, pack_text, interleaved_records
from run_native_preview import validate
from run_pmc_batch import Batch, LimitReached, Rejected, ROOT, PST, now, json_write, public_url


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def title_key(value):
    return re.sub(r"[^\w]+", "", value.casefold())


class NetworkUnavailable(LimitReached):
    """Stop on a persistent outage without consuming the candidate list."""


def continuation_deadline(config, original_end, current):
    continuation = config.get("authorized_continuation")
    if not continuation:
        return original_end
    if not continuation.get("user_instruction") or not continuation.get("authorized_at_pst"):
        raise ValueError("Continuation requires an explicit recorded user instruction")
    cutoff = datetime.fromisoformat(continuation["stop_before_pst"])
    if cutoff.tzinfo is None:
        raise ValueError("Continuation cutoff must include its timezone")
    return min(cutoff, current + timedelta(hours=continuation["maximum_session_hours"]))


class NativeScale(Batch):
    def __init__(self, config):
        self.tokenizer = Tokenizer.from_file(str(ROOT / config["tokenizer_path"]))
        self.overrides = json.loads((ROOT / config["citation_metadata_path"]).read_text())["papers"]
        self.titles = set()
        self.pdf_hashes = set()
        self.xml_hashes = set()
        super().__init__(config)
        self.end = continuation_deadline(config, self.end, datetime.now(PST))
        self.state["stop_at_pst"] = self.end.isoformat()
        if config.get("authorized_continuation"):
            self.state["authorized_continuation"] = config["authorized_continuation"]
        # A prior outage is historical; the new request will set live wait state.
        self.state.pop("network_outage", None)
        for p in self.state["papers"]:
            self.titles.add(title_key(p["title"]))
            self.pdf_hashes.add(p["pdf_sha256"])
            self.xml_hashes.add(p["xml_sha256"])
        self.persist()

    def wait_for_network(self, seconds):
        until = time.monotonic() + seconds
        while time.monotonic() < until:
            self.guard()
            time.sleep(min(5, max(0, until - time.monotonic())))

    def request(self, url, maximum, output=None):
        started = time.monotonic()
        wait = self.config.get("network_retry_initial_seconds", 30)
        maximum_wait = self.config.get("network_outage_budget_seconds", 1800)
        attempt = 0
        while True:
            self.guard()
            try:
                raw = super().request(url, maximum, output)
            except (URLError, TimeoutError) as exc:
                attempt += 1
                remaining = maximum_wait - (time.monotonic() - started)
                self.state["network_outage"] = {
                    "last_error": str(exc)[:240], "attempt": attempt,
                    "last_failure_at_pst": now(), "source_url": public_url(url),
                }
                if remaining <= 0:
                    raise NetworkUnavailable("Network outage recovery budget exhausted; pending candidate retained") from exc
                delay = min(wait, remaining)
                self.state["network_outage"]["retry_after_seconds"] = delay
                previous_stage = self.state.get("stage", "download_and_native_parse")
                self.state["stage"] = "waiting_for_network"
                self.event(f"NETWORK WAIT attempt={attempt} seconds={delay:.1f}; retrying the same request")
                self.wait_for_network(delay)
                self.state["stage"] = previous_stage
                wait = min(wait * 2, self.config.get("network_retry_maximum_seconds", 300))
            else:
                if self.state.pop("network_outage", None):
                    self.event("NETWORK RECOVERED; continuing the pending request")
                return raw

    def metadata(self, pmcid):
        meta, raw, url = super().metadata(pmcid)
        if re.search(self.config["excluded_method_title_pattern"], meta.get("title", ""), re.I):
            raise Rejected("Model/extraction-method title outside biology acquisition scope")
        if title_key(meta.get("title", "")) in self.titles:
            raise Rejected("Duplicate normalized title")
        return meta, raw, url

    def download(self, url, path, maximum):
        raw = path.read_bytes() if path.exists() else self.request(url, maximum, path)
        expected = parse_qs(urlsplit(url).query).get("md5", [""])[0]
        if expected and hashlib.md5(raw).hexdigest() != expected.zfill(32):
            raise ValueError("Source manifest MD5 mismatch")
        return raw

    def seed_cached(self):
        if self.state.get("cache_seed_complete"):
            return
        if not self.config.get("reuse_existing_sources", True):
            self.state["cache_seed_complete"] = True
            self.state["cache_policy"] = "Fresh acquisition; no prior batch sources or assets reused"
            self.persist()
            return
        prior = json.loads((ROOT / self.config["reuse_state"]).read_text())
        known = {p["pmcid"] for p in self.state["papers"]}
        for old in prior["papers"]:
            if old["pmcid"] in known:
                continue
            if re.search(self.config["excluded_method_title_pattern"], old["title"], re.I):
                self.state.setdefault("cache_scope_exclusions", []).append(
                    {"pmcid": old["pmcid"], "title": old["title"], "reason": "model/extraction-method title"})
                continue
            self.guard(32 * 2**20)
            out = self.dest / "papers" / old["pmcid"]
            out.mkdir(parents=True, exist_ok=True)
            for name in ["source.pdf", "source.xml", "source_metadata.json"]:
                src = ROOT / old["source_directory"] / name
                dst = out / name
                if not dst.exists():
                    os.link(src, dst)
            paper = copy.deepcopy(old)
            paper.update(source_directory=str(out.relative_to(ROOT)),
                         source_pdf=str((out / "source.pdf").relative_to(ROOT)),
                         source_xml=str((out / "source.xml").relative_to(ROOT)),
                         reused_from_batch=prior["batch_id"], prior_ocr_status=old["ocr_status"],
                         ocr_status="not_run_native_only", ocr_pages_completed=0,
                         acquired_at_pst=now())
            if digest(out / "source.pdf") != old["pdf_sha256"] or digest(out / "source.xml") != old["xml_sha256"]:
                raise ValueError("Cached source hash changed")
            # The legacy native view remains available alongside the new view.
            for name in ["native_document.json", "fullpaper_native.md", "source_evidence.jsonl"]:
                src = ROOT / old["source_directory"] / name
                dst = out / name
                if not dst.exists():
                    shutil.copyfile(src, dst)
            try:
                self.prepare(out, paper)
            except LimitReached:
                raise
            except Exception as exc:
                self.state.setdefault("cache_scope_exclusions", []).append(
                    {"pmcid": old["pmcid"], "title": old["title"], "reason": str(exc)})
                self.persist()
                continue
            self.state["papers"].append(paper)
            known.add(paper["pmcid"])
            self.register(paper)
            self.event("REUSED " + paper["pmcid"])
        self.state["cache_seed_complete"] = True
        self.persist()

    def register(self, paper):
        self.titles.add(title_key(paper["title"]))
        self.pdf_hashes.add(paper["pdf_sha256"])
        self.xml_hashes.add(paper["xml_sha256"])

    def save_native(self, out, paper, native):
        if paper["pdf_sha256"] in self.pdf_hashes or paper["xml_sha256"] in self.xml_hashes:
            raise Rejected("Duplicate PDF/XML content hash")
        if title_key(paper["title"]) in self.titles:
            raise Rejected("Duplicate normalized title")
        if re.search(self.config["excluded_method_title_pattern"], paper["title"], re.I):
            raise Rejected("Model/extraction-method title outside biology acquisition scope")
        super().save_native(out, paper, native)
        self.prepare(out, paper)
        self.register(paper)

    def prepare(self, out, paper):
        doc = parse_jats(out / "source.xml", paper["pmcid"], self.tokenizer,
                         citation_overrides=self.overrides.get(paper["pmcid"]),
                         maximum_table_rows=self.config["maximum_table_rows"])
        doc.update(journal=paper["journal"], license_code=paper["license_code"],
                   source_pdf=paper["source_pdf"], source_xml=paper["source_xml"],
                   source_pdf_sha256=paper["pdf_sha256"],
                   pmc_url=f"https://pmc.ncbi.nlm.nih.gov/articles/{paper['pmcid']}/")
        metadata = json.loads((out / "source_metadata.json").read_text())
        media = {Path(unquote(urlsplit(u).path)).name: u for u in metadata.get("media_urls", [])}
        assets = out / "assets"
        assets.mkdir(exist_ok=True)
        failures = []
        retained_figures = set()
        for visual in doc["visuals"]:
            visual["assets"] = []
            for href in visual["graphics"]:
                self.guard(self.config["maximum_asset_bytes"])
                filename = Path(href).name
                url = media.get(filename)
                if not url:
                    failures.append({"visual_id": visual["id"], "filename": filename,
                                     "reason": "no exact source-manifest filename"})
                    continue
                target = assets / filename
                cache_root = self.config.get("reuse_assets") if self.config.get("reuse_existing_sources", True) else None
                cache = ROOT / cache_root / paper["pmcid"] / "assets" / filename if cache_root else None
                try:
                    if not target.exists() and cache is not None and cache.exists():
                        os.link(cache, target)
                    raw = self.download(url, target, self.config["maximum_asset_bytes"])
                    expected = parse_qs(urlsplit(url).query).get("md5", [""])[0]
                    if expected and hashlib.md5(raw).hexdigest() != expected.zfill(32):
                        raise ValueError("media manifest MD5 mismatch")
                    visual["assets"].append({"path": str(target.relative_to(ROOT)),
                        "source_filename": filename, "source_url": public_url(url),
                        "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                        "manifest_md5": expected, "manifest_checksum_passed": bool(expected),
                        "binding": "exact source XML href and source media-manifest filename"})
                    if visual["kind"] == "figure":
                        retained_figures.add(filename)
                except LimitReached:
                    raise
                except Exception as exc:
                    failures.append({"visual_id": visual["id"], "filename": filename, "reason": str(exc)[:240]})
            visual["unresolved_media"] = visual["kind"] == "figure" and not visual["assets"]
        chunks = pack_text(doc, self.tokenizer, self.config["maximum_text_chunk_tokens"])
        groups = interleaved_records(doc)
        checks = validate(doc, chunks, groups, out / "source.xml")
        json_write(out / "document.json", doc)
        json_write(out / "validation.json", checks)
        for name, rows in [("text_chunks.jsonl", chunks), ("interleaved.jsonl", groups)]:
            (out / name).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        parts = ["# " + doc["title"]]
        last = None
        for block in doc["blocks"]:
            if block["section_path"] != last:
                parts.append("## " + " / ".join(block["section_path"]))
                last = block["section_path"]
            parts.append(block["training_text"])
        (out / "article.md").write_text("\n\n".join(parts) + "\n")
        figure_lines = ["# Source figures: " + doc["title"]]
        for visual in doc["visuals"]:
            if visual["kind"] == "figure":
                figure_lines.append("## " + (visual["label"] or visual["xml_id"]))
                for a in visual["assets"]:
                    figure_lines.append("![Original figure](assets/" + a["source_filename"] + ")")
                figure_lines.append(visual["caption_training_text"])
        (out / "figures.md").write_text("\n\n".join(figure_lines) + "\n")
        tables_dir = out / "tables"
        tables_dir.mkdir(exist_ok=True)
        for index, visual in enumerate(doc["visuals"]):
            if visual["table"]:
                safe = re.sub(r"[^\w.-]", "_", visual["xml_id"])
                (tables_dir / f"{index:03d}_{safe}.tsv").write_text(visual["table"]["text_tsv"] + "\n")
        paper.update(native_v4_status="completed", ocr_status="not_run_native_only", ocr_pages_completed=0,
                     figure_assets_retained=len(retained_figures), media_failures=failures,
                     figures_without_assets=sum(v["unresolved_media"] for v in doc["visuals"]),
                     text_chunks=len(chunks), text_tokens=sum(c["token_count"] for c in chunks),
                     full_source_table_cells=sum(len(v["table"]["cells"]) for v in doc["visuals"] if v["table"]),
                     bibliography_entries=len(doc["bibliography"]), citation_mentions=len(doc["citation_mentions"]),
                     processing="native source text/tables and original figures; no model inference")
        self.guard()

    def report(self):
        # Compact live reporting; no HTML site or bulk source files in Git.
        out = ROOT / self.config["report_directory"]
        out.mkdir(parents=True, exist_ok=True)
        papers = self.state["papers"]
        summary = {"batch_id": self.config["batch_id"], "updated_at_pst": now(),
            "status": self.state["status"], "stage": self.state.get("stage"),
            "target_papers": self.config["target_papers"], "ready_papers": len(papers),
            "target_reached": len(papers) >= self.config["target_papers"],
            "remaining_papers": max(0, self.config["target_papers"] - len(papers)),
            "reused_papers": sum(bool(p.get("reused_from_batch")) for p in papers),
            "figure_assets_retained": sum(p.get("figure_assets_retained", 0) for p in papers),
            "figures_without_assets": sum(p.get("figures_without_assets", 0) for p in papers),
            "media_failures": sum(len(p.get("media_failures", [])) for p in papers),
            "total_text_tokens": sum(p.get("text_tokens", 0) for p in papers),
            "total_text_chunks": sum(p.get("text_chunks", 0) for p in papers),
            "total_main_article_tables": sum(p.get("tables", 0) for p in papers),
            "total_source_table_cells": sum(p.get("full_source_table_cells", 0) for p in papers),
            "downloaded_response_bytes": self.state["downloaded_response_bytes"],
            "logical_artifact_bytes": self.state.get("artifact_bytes", 0),
            "journal_counts": dict(Counter(p["journal"] for p in papers)),
            "gpu_count": 0, "model_inference": False, "model_training": False,
            "stop_at_pst": self.state.get("stop_at_pst"),
            "limit_reason": self.state.get("limit_reason"), "error": self.state.get("error"),
            "authorized_continuation": self.state.get("authorized_continuation"),
            "network_outage": self.state.get("network_outage"),
            "maximum_download_bytes": self.config["maximum_download_bytes"],
            "maximum_artifact_bytes": self.config["maximum_artifact_bytes"],
            "fresh_acquisition": not self.config.get("reuse_existing_sources", True),
            "tokenizer_path": self.config["tokenizer_path"],
            "historical_connection_refused_attempts": sum("Connection refused" in r.get("reason", "") for r in self.state["rejected"]),
            "scope": "native XML text/full source tables and original figure assets; separate supplements not downloaded",
            "limitations": ["Topic-selected convenience sample, not representative sampling.",
                "Source checks do not validate biological figure interpretation.",
                "Unresolved/oversized/failed media remain explicitly listed.",
                "Prior outputs and model caches are retained; this batch runs no new OCR."]}
        json_write(out / "summary.json", summary)
        fields = ["pmcid", "journal", "title", "doi", "native_v4_status", "reused_from_batch",
                  "pdf_pages", "figures", "tables", "figure_assets_retained", "figures_without_assets",
                  "text_tokens", "text_chunks", "full_source_table_cells", "license_code", "source_directory"]
        with (out / "papers.csv").open("w", newline="") as f:
            w = csv.DictWriter(f, fields, extrasaction="ignore");w.writeheader();w.writerows(papers)
        if summary["fresh_acquisition"]:
            run_note = ("This is a fresh, independent 500-paper acquisition. No documents or assets are "
                        "seeded from prior batches, and prior progress does not count toward this target. "
                        "Duplicates are removed within this run. Original prior outputs remain unchanged.\n\n")
        else:
            run_note = ("The first run stopped at 295 papers after connection failures. The user authorized continuing "
                        "on October 15; existing papers and cumulative response-byte/storage counters are retained. "
                        "The earlier candidate-pool status did not establish exhaustion of eligible PMC papers.\n\n")
        (out / "README.md").write_text(
            "# " + self.config.get("report_title", "500-paper biological source batch") + "\n\n"
            f"Status: **{summary['status']}**; {len(papers)}/{self.config['target_papers']} papers ready. "
            f"Updated {summary['updated_at_pst']} (fixed PST).\n\n"
            f"Original figure assets retained: **{summary['figure_assets_retained']}**. "
            f"Figure records without assets: **{summary['figures_without_assets']}**.\n\n"
            f"Extracted text: **{summary['total_text_tokens']:,} tokens** in {summary['total_text_chunks']:,} chunks; "
            f"main-article tables: **{summary['total_main_article_tables']:,}**.\n\n"
            "[Paper manifest](papers.csv) · [Exact summary and limits](summary.json)\n\n"
            + run_note
            + f"Run cutoff: **{summary['stop_at_pst']}** (fixed PST). Transient failures retry the same request with backoff.\n\n"
            f"Cumulative downloaded response bodies: **{summary['downloaded_response_bytes'] / 2**30:.2f} GiB / {self.config['maximum_download_bytes'] / 2**30:g} GiB**; "
            f"logical artifacts: **{summary['logical_artifact_bytes'] / 2**30:.2f} GiB / {self.config['maximum_artifact_bytes'] / 2**30:g} GiB**.\n\n"
            "Full PDF/XML, source images, extracted text, source-table TSVs and structured citation/context "
            "records stay in the run's source_directory listed in the manifest. "
            "This batch runs one serial CPU/network worker, no OCR, no recaptioning and no training. "
            "Separate supplementary files are not downloaded. Prior outputs remain unchanged.\n")

    def finish_exports(self):
        self.report()

    def run(self):
        try:
            self.seed_cached()
            self.acquire()
            self.state.update(status="completed" if len(self.state["papers"]) >= self.config["target_papers"] else "candidate_pool_exhausted",
                              stage="finished", finished_at_pst=now())
        except NetworkUnavailable as exc:
            self.state.update(status="network_unavailable", stage="finished", error=str(exc), finished_at_pst=now())
        except LimitReached as exc:
            self.state.update(status="limited", stage="finished", limit_reason=str(exc), finished_at_pst=now())
        except Exception as exc:
            self.state.update(status="failed", stage="finished", error=type(exc).__name__ + ": " + str(exc), finished_at_pst=now())
            raise
        finally:
            self.persist()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, required=True)
    args = ap.parse_args()
    config = json.loads(args.config.read_text())
    if config["document_workers"] != 1 or config["gpu_count"] != 0:
        raise ValueError("Native scale batch is serial and CPU only")
    NativeScale(config).run()


if __name__ == "__main__":
    main()
