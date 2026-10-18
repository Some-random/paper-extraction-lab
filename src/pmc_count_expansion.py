"""Serial PMC native-XML acquisition inside the existing census budget/lock."""
from __future__ import annotations

import gzip
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import parse_qs, quote, unquote, urlencode, urlsplit, urlunsplit

import requests
from lxml import etree

from corpus_count import canonical_paper_text, sha256
from native_training import parse_jats

S3 = "https://pmc-oa-opendata.s3.amazonaws.com"
ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
BIOLOGY = {
    "gene": r"\bgene\w*|\bgenom\w*|\bRNA\b|\bDNA\b|\btranscript\w*",
    "protein": r"\bprotein\w*|\bpeptide\w*|\benzyme\w*|\bantibod\w*",
    "organism": r"\bmice\b|\bmouse\b|\bbacter\w*|\bplant\w*|\bfung\w*|\bmicrob\w*|\bneur\w*|\bspecies\b|\bevolut\w*",
    "cell": r"\bcells?\b|\bcellular\b|\btissue\w*|\bmetaboli\w*|\bimmun\w*|\becolog\w*",
}


class RejectedPaper(Exception):
    pass


class PaperBudgetReached(Exception):
    pass


def clinical_title_reason(title):
    if re.search(r"\bclinical (?:decision|trial|practice|management)\b|\bburden of illness\b|"
                 r"\btherapeutic options\b|\bcardioverter defibrillator\b|\bcase reports?\b|"
                 r"\bdiagnostic accuracy\b|\btreatment guidelines?\b|"
                 r"\b(?:randomi[sz]ed|controlled|non[-‐‑– ]inferiority|open[-‐‑– ]label)\b.{0,100}\btrial\b",
                 title, re.I):
        return "Explicit clinical care/trial/device title outside research-biology selection"
    return None


def public_url(value):
    parts = urlsplit(value)
    if parts.scheme == "s3":
        return urlunsplit(("https", parts.netloc + ".s3.amazonaws.com",
                           quote(unquote(parts.path), safe="/"), parts.query, ""))
    return value


def choose_metadata(options):
    valid = [m for m in options if m.get("xml_url") and str(m.get("is_retracted", "no")).lower() not in {"yes", "true", "1"}]
    if not valid:
        raise RejectedPaper("No non-retracted distributed XML version")
    return min(valid, key=lambda m: (str(m.get("is_manuscript", "no")).lower() in {"yes", "true", "1"},
                                     -int(m.get("version", 1))))


def biology_markers(document):
    value = document["title"] + " " + " ".join(b["text"] for b in document["blocks"] if b["kind"] == "abstract")
    return [key for key, pattern in BIOLOGY.items() if re.search(pattern, value, re.I)]


class PaperExpansion:
    def __init__(self, worker):
        self.worker = worker
        self.plan = worker.paper_plan
        self.root = worker.run / "pmc_expansion"
        self.root.mkdir(parents=True, exist_ok=True)
        self.progress = worker.state.setdefault("paper_expansion", {})
        self.progress.setdefault("started_at_pst", worker.state["updated_at_pst"])
        self.progress.setdefault("started_epoch", time.time())
        self.progress.setdefault("downloaded_bytes", 0)
        self.progress.setdefault("reserved_bytes", 0)
        self.progress.setdefault("cursor", 0)
        self.progress.setdefault("rejected", 0)
        self.progress["target_new_papers"] = self.plan["target_new_papers"]
        self.session = requests.Session()
        self.session.headers.update({"Accept-Encoding": "identity", "User-Agent": "paper-extraction-lab/PMC-census (serial)"})
        self.overrides = json.loads((worker.config_path.parent / "pmc_citation_metadata.json").read_text())["papers"]
        self.known_ids = set()
        self.known_dois = set()
        for row in worker.ledger.db.execute("SELECT r.provenance FROM records r JOIN files f ON f.id=r.file_id WHERE f.source='pmc'"):
            provenance = json.loads(row[0])
            if provenance.get("id"):
                self.known_ids.add(provenance["id"])
            if provenance.get("doi"):
                self.known_dois.add(provenance["doi"].strip().lower())
        worker.persist()

    def fetch(self, url, path, maximum):
        """Small bounded HTTP object, with shared cumulative byte accounting."""
        if path.exists():
            return path.read_bytes()
        path.parent.mkdir(parents=True, exist_ok=True)
        for attempt in range(3):
            self.worker.guard()
            global_left = self.worker.config["limits"]["network_reserved_bytes"] - self.worker.state["network_reserved_bytes"]
            phase_left = self.plan["maximum_new_paper_download_bytes"] - self.progress["reserved_bytes"]
            admitted = min(maximum, global_left, phase_left)
            if admitted <= 0:
                raise PaperBudgetReached("paper_download_budget")
            if self.worker.state["new_artifact_bytes"] + admitted + 8 * 2**20 > self.worker.config["limits"]["new_artifact_bytes"]:
                raise PaperBudgetReached("paper_artifact_budget")
            self.worker.state["network_reserved_bytes"] += admitted
            self.progress["reserved_bytes"] += admitted
            self.worker.persist()
            received = 0
            try:
                with self.session.get(url, stream=True, timeout=(15, 35)) as response:
                    if response.status_code == 404:
                        raise RejectedPaper("Distributed object not found")
                    response.raise_for_status()
                    length = int(response.headers.get("Content-Length", "0"))
                    if length > admitted:
                        if admitted < maximum:
                            raise PaperBudgetReached("paper_download_budget_for_next_object")
                        raise RejectedPaper("Object exceeds configured byte limit")
                    chunks = []
                    while received < admitted:
                        self.worker.guard()
                        block = response.raw.read(min(65536, admitted - received), decode_content=False)
                        if not block:
                            break
                        chunks.append(block)
                        received += len(block)
                    if length and received != length:
                        raise OSError("Incomplete PMC response")
                    if not length and received == admitted:
                        raise RejectedPaper("Response reached byte cap without verified end")
                    raw = b"".join(chunks)
                temporary = path.with_suffix(path.suffix + ".part")
                temporary.write_bytes(raw)
                temporary.replace(path)
                return raw
            except (requests.RequestException, OSError) as exc:
                if attempt == 2:
                    raise RuntimeError("PMC transport failed after three attempts: " + type(exc).__name__) from None
                time.sleep(1)
            finally:
                # Unused reservation is refunded after a bounded completed
                # operation. A hard crash leaves the conservative reservation.
                self.worker.state["network_reserved_bytes"] -= admitted - received
                self.progress["reserved_bytes"] -= admitted - received
                self.worker.state["network_body_bytes"] += received
                self.progress["downloaded_bytes"] += received
                self.worker.persist()

    def candidates(self):
        path = self.root / "candidates.json"
        if path.exists():
            return json.loads(path.read_text())["candidates"]
        strata = []
        queries = []
        for topic, terms in self.plan["topics"].items():
            for first, last in self.plan["years"]:
                biology = "(" + " OR ".join(term + "[tiab]" for term in terms) + ")"
                query = (biology + f" AND {first}:{last}[pdat] AND (open_access[filter] OR author_manuscript[filter])"
                         ' NOT "pmc embargo"[filter] NOT (articletyperetraction OR articletypecorrection OR hasretractionin)')
                url = ESEARCH + "?" + urlencode({"db": "pmc", "term": query, "retmode": "json",
                         "retmax": self.plan["candidates_per_stratum"], "tool": "paper_extraction_lab"})
                raw = self.fetch(url, self.root / "api" / f"{topic}_{first}_{last}.json", 2**20)
                response = json.loads(raw)
                result = response["esearchresult"]
                if response.get("error") or result.get("error") or result.get("errorlist") or result.get("warninglist", {}).get("quotedphrasesnotfound"):
                    raise ValueError("PMC candidate query needs correction: " + topic + " " + str(first))
                ids = ["PMC" + str(uid).removeprefix("PMC") for uid in result["idlist"]]
                ids.sort(key=lambda uid: hashlib.sha256((topic + str(first) + uid).encode()).hexdigest())
                strata.append([{"pmcid": uid, "stratum": topic + "_" + str(first)} for uid in ids])
                queries.append({"query": query, "url": url, "matches": int(result["count"]), "returned": len(ids),
                                "response_sha256": hashlib.sha256(raw).hexdigest()})
                time.sleep(0.4)
                self.worker.publish()
        seen = set(self.known_ids)
        candidates = []
        for index in range(max(map(len, strata), default=0)):
            for group in strata:
                if index < len(group) and group[index]["pmcid"] not in seen:
                    seen.add(group[index]["pmcid"])
                    candidates.append(group[index])
        self.worker.write_json(path, {"candidates": candidates, "queries": queries,
            "selection": "Fixed interleaving of topic/year search-return subsets, shuffled deterministically within each stratum; convenience collection, not probability sampling."})
        return candidates

    def metadata(self, pmcid, directory):
        url = S3 + "/?" + urlencode({"list-type": 2, "prefix": "metadata/" + pmcid + "."})
        raw = self.fetch(url, directory / "versions.xml", 2**19)
        listing = etree.fromstring(raw, etree.XMLParser(resolve_entities=False, no_network=True))
        if listing.findtext("{*}IsTruncated") == "true":
            raise ValueError("PMC version listing unexpectedly truncated")
        options = []
        for key in listing.findall(".//{*}Key"):
            if key.text and key.text.endswith(".json"):
                data = self.fetch(S3 + "/" + key.text, directory / Path(key.text).name, 2**19)
                row = json.loads(data)
                if str(row.get("pmcid", "")).removeprefix("PMC") != pmcid.removeprefix("PMC"):
                    raise ValueError("PMC metadata identity mismatch")
                options.append(row)
        chosen = choose_metadata(options)
        self.worker.write_json(directory / "selected_metadata.json", chosen)
        return chosen

    def acquire(self, candidate):
        pmcid = candidate["pmcid"]
        directory = self.root / "papers" / pmcid
        directory.mkdir(parents=True, exist_ok=True)
        metadata = self.metadata(pmcid, directory)
        doi = (metadata.get("doi") or "").strip().lower()
        if doi and doi in self.known_dois:
            raise RejectedPaper("DOI already represented in the paper collection")
        title = metadata.get("title") or ""
        if clinical_title_reason(title):
            raise RejectedPaper(clinical_title_reason(title))
        if re.search(r"large language|foundation model|optical character recognition|document extraction", title, re.I):
            raise RejectedPaper("Model/extraction-method paper outside acquisition scope")
        url = public_url(metadata["xml_url"])
        source = directory / "source.xml"
        raw = self.fetch(url, source, self.plan["maximum_xml_bytes"])
        expected = parse_qs(urlsplit(url).query).get("md5", [None])[0]
        if not expected or hashlib.md5(raw).hexdigest().lower() != expected.lower():
            raise ValueError("PMC XML checksum mismatch; retained source requires inspection")
        tree = etree.fromstring(raw, etree.XMLParser(resolve_entities=False, no_network=True))
        if etree.QName(tree).localname != "article" or tree.get("article-type") not in self.plan["accepted_article_types"]:
            raise RejectedPaper("Non-selected JATS article type")
        try:
            document = parse_jats(source, pmcid, self.worker.tokenizer, citation_overrides=self.overrides.get(pmcid),
                                  maximum_table_rows=self.plan["maximum_table_rows"])
        except ValueError as exc:
            raise RejectedPaper("Native parser requires review: " + str(exc)) from None
        if document["duplicate_visual_ids"]:
            raise RejectedPaper("Native XML contains ambiguous duplicate visual identifiers")
        markers = biology_markers(document)
        if len(markers) < 2 or not {"gene", "protein", "organism"}.intersection(markers):
            raise RejectedPaper("Insufficient research-biology title/abstract markers")
        text = canonical_paper_text(document)
        body = " ".join(b["text"] for b in document["blocks"] if b.get("region") == "body")
        if len(body) < 500:
            raise RejectedPaper("Insufficient native article body")
        if len(text.encode()) > self.worker.config["limits"]["maximum_text_bytes"]:
            raise RejectedPaper("Canonical paper exceeds text byte cap; not truncated")
        document.update(source_xml=str(source.relative_to(self.worker.config_path.parents[1])),
                        source_metadata=metadata, biology_markers=markers,
                        media_status="Source URLs/links retained; binary PDF/media/supplements deferred for bounded text census")
        parsed = directory / "document.json.gz"
        parsed.write_bytes(gzip.compress(json.dumps(document, ensure_ascii=False).encode(), mtime=0))
        record = {"id": pmcid, "text": text, "doi": doi or None,
                  "version": metadata.get("version"), "license": metadata.get("license_code"),
                  "source_xml_sha256": hashlib.sha256(raw).hexdigest(),
                  "source_document": str(parsed.relative_to(self.worker.config_path.parents[1])),
                  "source_document_sha256": sha256(parsed), "url": url, "images": 0,
                  "article_type": tree.get("article-type"), "biology_markers": markers,
                  "selection_stratum": candidate["stratum"], "media_status": "deferred_source_urls_retained"}
        canonical = directory / "canonical.jsonl"
        canonical.write_text(json.dumps(record, ensure_ascii=False) + "\n")
        return {"id": "pmc_new_" + pmcid, "source": "pmc", "path": str(canonical),
                "format": "jsonl", "bytes": canonical.stat().st_size, "sha256": sha256(canonical),
                "expected_records": 1, "pmcid": pmcid, "doi": doi or None,
                "source_xml_sha256": record["source_xml_sha256"], "extension": "pmc_expansion"}

    def run(self):
        self.progress["status"] = "acquiring_native_papers"
        self.worker.state["current_file"] = "pmc_candidate_discovery"
        self.worker.persist()
        self.worker.publish()
        try:
            candidates = self.candidates()
            for index in range(self.progress["cursor"], len(candidates)):
                self.worker.guard()
                accepted = sum(item.get("extension") == "pmc_expansion" and
                    self.worker.ledger.file_state(item["id"])[0] == "complete" for item in self.worker.config["files"])
                self.progress["accepted_new_papers"] = accepted
                if accepted >= self.plan["target_new_papers"]:
                    self.progress.update(status="target_reached")
                    break
                if time.time() >= self.progress["started_epoch"] + self.plan["maximum_phase_seconds"]:
                    self.progress.update(status="phase_time_limit")
                    break
                candidate = candidates[index]
                pmcid = candidate["pmcid"]
                self.progress["current_pmcid"] = pmcid
                self.worker.state["current_file"] = "acquiring_" + pmcid
                if pmcid in self.known_ids:
                    self.progress["cursor"] = index + 1
                    continue
                try:
                    item = self.acquire(candidate)
                    self.worker.ledger.register_extension(item)
                    self.worker.config["files"].append(item)
                    self.worker.refresh_paper_source()
                    self.worker.state["current_file"] = item["id"]
                    self.worker.count(item, self.worker.acquire(item))
                    self.known_ids.add(pmcid)
                    if item.get("doi"):
                        self.known_dois.add(item["doi"])
                    self.progress["accepted_new_papers"] = accepted + 1
                except (RejectedPaper, etree.XMLSyntaxError) as exc:
                    self.progress["rejected"] += 1
                    with (self.root / "rejected.jsonl").open("a") as out:
                        out.write(json.dumps({**candidate, "reason": str(exc), "at_pst": self.worker.state["updated_at_pst"]}) + "\n")
                self.progress["cursor"] = index + 1
                self.worker.persist()
                if time.monotonic() - self.worker.last_published >= 30:
                    self.worker.publish()
            else:
                self.progress["status"] = "candidate_subsets_exhausted"
        except PaperBudgetReached as exc:
            self.progress.update(status=str(exc))
        finally:
            self.session.close()
            self.worker.persist()
            self.worker.publish()
