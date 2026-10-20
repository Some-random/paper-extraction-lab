#!/bin/bash
#SBATCH --job-name=bio-paper-continue
#SBATCH --partition=il-cpu
#SBATCH --account=infolab
#SBATCH --qos=il-cpu
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=1-00:00:00
#SBATCH --requeue
#SBATCH --signal=B:USR1@180
#SBATCH --open-mode=append
#SBATCH --chdir=/dfs/scratch0/dongweij/paper-extraction-lab
#SBATCH --output=/dfs/scratch0/dongweij/paper-extraction-lab/experiments/paper_collection_continuation_2026-10-20/worker.log

set -euo pipefail
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
export TOKENIZERS_PARALLELISM=false PYTHONDONTWRITEBYTECODE=1
continuation_pid=""
checkpoint_signal_received=0
forward_checkpoint() {
    checkpoint_signal_received=1
    if [[ -n "$continuation_pid" ]]; then
        kill -USR1 "$continuation_pid" 2>/dev/null || true
    fi
}
trap forward_checkpoint USR1
.review-venv/bin/python -B -u scripts/run_paper_collection_continuation.py \
    --config config/paper_collection_continuation_2026-10-20.json &
continuation_pid=$!
set +e
while true; do
    wait "$continuation_pid"
    continuation_status=$?
    if ! kill -0 "$continuation_pid" 2>/dev/null; then
        break
    fi
done
if [[ "$checkpoint_signal_received" -eq 1 && "$continuation_status" -ge 128 ]]; then
    # A trapped signal can interrupt wait just as the child finishes. Retrieve
    # its remembered exit status so a completed checkpoint is not mistaken for
    # the shell's interrupted-wait status.
    wait "$continuation_pid"
    continuation_status=$?
fi
set -e
if [[ "$continuation_status" -eq 75 ]]; then
    scontrol requeue "$SLURM_JOB_ID"
    exit 0
fi
exit "$continuation_status"
