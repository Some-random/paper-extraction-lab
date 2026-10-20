#!/bin/bash
#SBATCH --job-name=bio4b-a100-opt
#SBATCH --account=infolab
#SBATCH --partition=il
#SBATCH --qos=il
#SBATCH --nice=0
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:a100:8
#SBATCH --cpus-per-task=64
#SBATCH --mem=384G
#SBATCH --time=02:00:00
#SBATCH --signal=B:TERM@60
#SBATCH --no-requeue
#SBATCH --output=experiments/training_throughput_2026-10-18/slurm-%j.log

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
export TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 WANDB_DISABLED=true
export TORCHINDUCTOR_COMPILE_THREADS=2
optimization_job_dir="$SLURM_SUBMIT_DIR/experiments/training_throughput_2026-10-18/job_$SLURM_JOB_ID"
mkdir -p "$optimization_job_dir/compile_cache/tmp"
export TORCHINDUCTOR_CACHE_DIR="$optimization_job_dir/compile_cache/torchinductor"
export TRITON_CACHE_DIR="$optimization_job_dir/compile_cache/triton"
export CUTE_DSL_CACHE_DIR="$optimization_job_dir/compile_cache/cute"
export CUDA_CACHE_PATH="$optimization_job_dir/compile_cache/cuda"
export XDG_CACHE_HOME="$optimization_job_dir/compile_cache/xdg"
export TMPDIR="$optimization_job_dir/compile_cache/tmp"
export CUDA_CACHE_MAXSIZE=1073741824
exec .b200-opt-venv/bin/python -B -u scripts/benchmark_gpu_sweep.py \
  --config config/a100_optimization_2026-10-20.json \
  --world-size 8 --gpu-type a100 --output-dir "$optimization_job_dir"
