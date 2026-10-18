#!/bin/bash
#SBATCH --job-name=bio4b-throughput
#SBATCH --account=infolab
#SBATCH --partition=il
#SBATCH --qos=il-lo
#SBATCH --nice=10000
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:a100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --time=00:20:00
#SBATCH --no-requeue
#SBATCH --output=experiments/training_throughput_2026-10-18/slurm-%j.log

set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
benchmark_run=experiments/training_throughput_2026-10-18
benchmark_job="$benchmark_run/job_$SLURM_JOB_ID"
mkdir -p "$benchmark_job"

finish_benchmark() {
  benchmark_exit=$?
  trap - EXIT
  .review-venv/bin/python - "$SLURM_JOB_ID" "$benchmark_exit" <<'PY'
import datetime, json, sys
from pathlib import Path
job_id, code = sys.argv[1], int(sys.argv[2])
base = Path('experiments/training_throughput_2026-10-18')
launch = base / f'launch_{job_id}.json'
state = json.loads(launch.read_text()) if launch.exists() else {'job_id': job_id}
result = base / f'job_{job_id}/results.json'
if result.exists():
    state['status'] = json.loads(result.read_text()).get('status', 'failed')
else:
    state['status'] = 'failed'
state['exit_code'] = code
state['finished_at_pst'] = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-8))).isoformat()
launch.write_text(json.dumps(state, indent=2) + '\n')
PY
  .review-venv/bin/python scripts/report_training_throughput.py --publish || true
  exit "$benchmark_exit"
}
trap finish_benchmark EXIT
trap 'exit 143' TERM

.review-venv/bin/python - "$SLURM_JOB_ID" <<'PY'
import datetime, json, os, sys
from pathlib import Path
base = Path('experiments/training_throughput_2026-10-18')
path = base / f'launch_{sys.argv[1]}.json'
state = json.loads(path.read_text()) if path.exists() else {'job_id': sys.argv[1]}
state.update(status='running', started_at_pst=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-8))).isoformat(),
             results_path=str(base / f'job_{sys.argv[1]}/results.json'), requested_gpus=int(os.environ.get('SLURM_GPUS_ON_NODE', '1')))
path.write_text(json.dumps(state, indent=2) + '\n')
PY

export OMP_NUM_THREADS=2
export MKL_NUM_THREADS=2
export TOKENIZERS_PARALLELISM=false
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export WANDB_DISABLED=true
export TORCHINDUCTOR_CACHE_DIR="$SLURM_SUBMIT_DIR/cache/throughput_inductor"
benchmark_world="${SLURM_GPUS_ON_NODE:-1}"

if [ "$benchmark_world" -eq 1 ]; then
  .throughput-venv/bin/python -u scripts/benchmark_4b_training.py \
    --model-config config/qwen3_4b_throughput_model.json \
    --output "$benchmark_job/results.json"
else
  .throughput-venv/bin/python -u -m torch.distributed.run \
    --standalone --nnodes=1 --nproc_per_node="$benchmark_world" --max-restarts=0 \
    scripts/benchmark_4b_training.py \
    --model-config config/qwen3_4b_throughput_model.json \
    --output "$benchmark_job/results.json"
fi
