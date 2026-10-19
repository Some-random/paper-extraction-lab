#!/bin/bash
#SBATCH --job-name=bio-paper-collect
#SBATCH --partition=il-cpu
#SBATCH --account=infolab
#SBATCH --qos=il-cpu
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=1-00:05:00
#SBATCH --chdir=/dfs/scratch0/dongweij/paper-extraction-lab
#SBATCH --output=/dfs/scratch0/dongweij/paper-extraction-lab/experiments/paper_collection_2026-10-19/worker.log

set -euo pipefail
export OMP_NUM_THREADS=2
export OPENBLAS_NUM_THREADS=2
export MKL_NUM_THREADS=2
export TOKENIZERS_PARALLELISM=false
exec .review-venv/bin/python -B -u scripts/run_paper_collection.py --config config/paper_collection_2026-10-19.json
