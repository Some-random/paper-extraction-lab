"""Download a tiny, explicit corpus sequentially and record exact source hashes."""
import hashlib
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PST = timezone(timedelta(hours=-8))
SOURCES = [
    ("ryze", "Ryze: Evidence-Enriched Data Synthesis from Biomedical Papers", "pdf",
     "https://arxiv.org/pdf/2606.00902v1"),
    ("llava_med", "LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine in One Day", "pdf",
     "https://arxiv.org/pdf/2306.00890v1"),
    ("affibody", "The Influence of Domain Permutations of an Albumin-Binding Domain-Fused HER2-Targeting Affibody-Based Drug Conjugate on Tumor Cell Proliferation and Therapy Efficacy", "xml",
     "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC8617914/fullTextXML"),
    ("affibody", "The Influence of Domain Permutations of an Albumin-Binding Domain-Fused HER2-Targeting Affibody-Based Drug Conjugate on Tumor Cell Proliferation and Therapy Efficacy", "pdf",
     "https://mdpi-res.com/d_attachment/pharmaceutics/pharmaceutics-13-01974/article_deploy/pharmaceutics-13-01974.pdf"),
]
REFERENCES = [
    ("ryze_readme.md", "https://raw.githubusercontent.com/Chivier/Ryze-Data/main/README.md"),
    ("olmocr_readme.md", "https://raw.githubusercontent.com/allenai/olmocr/main/README.md"),
    ("olmocr_prompt.py", "https://raw.githubusercontent.com/allenai/olmocr/main/olmocr/prompts/prompts.py"),
    ("docling_example.py", "https://raw.githubusercontent.com/docling-project/docling/main/docs/examples/export_figures.py"),
    ("olmo3.html", "https://arxiv.org/html/2512.13961v2"),
]


def fetch(url, target):
    if not target.exists():
        temporary = target.with_suffix(target.suffix + ".part")
        subprocess.run(["curl", "-fsSL", "--connect-timeout", "15", "--max-time", "120",
                        url, "-o", str(temporary)], check=True)
        temporary.replace(target)
    return hashlib.sha256(target.read_bytes()).hexdigest()


def main():
    records = []
    for doc_id, title, fmt, url in SOURCES:
        target = ROOT / "inputs" / f"{doc_id}.{fmt}"
        digest = fetch(url, target)
        if fmt == "pdf" and not target.read_bytes().startswith(b"%PDF-"):
            raise ValueError(f"Not a PDF: {target}")
        records.append(dict(id=doc_id, title=title, format=fmt, url=url,
                            path=str(target.relative_to(ROOT)), sha256=digest,
                            bytes=target.stat().st_size))
        print(doc_id, fmt, target.stat().st_size, flush=True)
    for filename, url in REFERENCES:
        try:
            digest = fetch(url, ROOT / "sources" / filename)
            records.append(dict(id=filename, format="method_reference", url=url,
                                path="sources/" + filename, sha256=digest))
        except subprocess.CalledProcessError as exc:
            records.append(dict(id=filename, url=url, error=str(exc)))
    (ROOT / "inputs" / "manifest.json").write_text(json.dumps({
        "created_at_pst": datetime.now(PST).isoformat(), "download_workers": 1,
        "sources": records,
    }, indent=2) + "\n")


if __name__ == "__main__":
    main()
