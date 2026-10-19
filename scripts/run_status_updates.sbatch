#!/bin/bash
#SBATCH --job-name=bio-status-updates
#SBATCH --partition=il-cpu
#SBATCH --account=infolab
#SBATCH --qos=il-cpu
#SBATCH --nodelist=furiosa
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=7-00:00:00
#SBATCH --chdir=/dfs/scratch0/dongweij/paper-extraction-lab
#SBATCH --output=/dfs/scratch0/dongweij/paper-extraction-lab/experiments/chat_updates_2026-10-19/supervisor.log

set -euo pipefail
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export MKL_NUM_THREADS=1
exec .review-venv/bin/python -B -u scripts/supervise_status_updates.py \
  --config experiments/chat_updates_2026-10-19/config.json
