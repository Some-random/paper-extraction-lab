#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export CUDA_VISIBLE_DEVICES=''
export OMP_NUM_THREADS=2
export OPENBLAS_NUM_THREADS=2
export MKL_NUM_THREADS=2
export PYTHONUNBUFFERED=1
export PIP_CACHE_DIR="$PWD/cache/pip"
python3 scripts/download_samples.py
.venv/bin/python scripts/prepare_scan.py
.venv/bin/python scripts/prepare_scan.py --doc affibody --page 11 --output-id affibody_scan_p11
.venv/bin/python src/extract_native.py
.venv/bin/python src/extract_docling.py --doc ryze --doc llava_med --doc affibody
.venv/bin/python src/extract_docling.py --doc ryze_scan_p5 --ocr
.venv/bin/python src/extract_docling.py --doc affibody_scan_p11 --ocr
.venv/bin/python src/build_samples.py
.venv/bin/python src/build_hybrid.py
.venv/bin/python src/export_hybrid_qa.py
.venv/bin/python src/audit_samples.py
.venv/bin/python scripts/check_targeted_ocr.py
.venv/bin/python scripts/finalize_report.py
