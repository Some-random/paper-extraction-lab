#!/bin/bash
#SBATCH --job-name=bio-corpus-count
#SBATCH --partition=il-cpu
#SBATCH --account=infolab
#SBATCH --qos=il-cpu-long
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=12:05:00
#SBATCH --chdir=/dfs/scratch0/dongweij/paper-extraction-lab
#SBATCH --output=/dfs/scratch0/dongweij/paper-extraction-lab/experiments/corpus_count_2026-10-17/worker.log

set -euo pipefail
export OMP_NUM_THREADS=2
export OPENBLAS_NUM_THREADS=2
export MKL_NUM_THREADS=2
export TOKENIZERS_PARALLELISM=false
exec .review-venv/bin/python -u scripts/run_corpus_count.py
