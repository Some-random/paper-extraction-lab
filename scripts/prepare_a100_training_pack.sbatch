#!/bin/bash
#SBATCH --job-name=bio4b-token-pack
#SBATCH --account=infolab
#SBATCH --partition=il-cpu
#SBATCH --qos=il-cpu
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=01:05:00
#SBATCH --no-requeue
#SBATCH --output=experiments/a100_optimization_2026-10-20/pack-%j.log

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
export PYTHONDONTWRITEBYTECODE=1 TOKENIZERS_PARALLELISM=false
exec .b200-opt-venv/bin/python -B -u scripts/prepare_training_token_pack.py \
  --source-config config/paper_collection_2026-10-19.json \
  --tokenizer-path cache/tokenizers/qwen3-4b-base-906bfd4b4dc7f14ee4320094d8b41684abff8539/tokenizer.json \
  --tokenizer-sha256 c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539 \
  --output-dir experiments/a100_optimization_2026-10-20/token_pack
