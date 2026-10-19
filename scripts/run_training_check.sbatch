#!/bin/bash
#SBATCH --job-name=bio4b-verify
#SBATCH --account=infolab
#SBATCH --partition=il
#SBATCH --qos=il
#SBATCH --nice=0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:b200:2
#SBATCH --cpus-per-task=24
#SBATCH --mem=192G
#SBATCH --time=00:20:00
#SBATCH --no-requeue
#SBATCH --output=experiments/training_throughput_2026-10-18/slurm-%j.log

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
export TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 WANDB_DISABLED=true

check_gpu_type="$1"
check_mode="$2"
check_job_dir="experiments/training_throughput_2026-10-18/job_$SLURM_JOB_ID"
mkdir -p "$check_job_dir"
exec .throughput-venv/bin/python -B -u scripts/benchmark_training_check.py \
  --config config/training_throughput_check_2026-10-19.json \
  --world-size "$SLURM_GPUS_ON_NODE" --gpu-type "$check_gpu_type" \
  --output-dir "$check_job_dir" --mode "$check_mode"
