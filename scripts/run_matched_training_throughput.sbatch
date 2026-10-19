#!/bin/bash
#SBATCH --job-name=bio4b-match
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
benchmark_run=experiments/training_throughput_2026-10-18
benchmark_job="$benchmark_run/job_$SLURM_JOB_ID"
mkdir -p "$benchmark_job"
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=2 MKL_NUM_THREADS=2
export TOKENIZERS_PARALLELISM=false HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 WANDB_DISABLED=true

finish_benchmark() {
  benchmark_exit=$?
  trap - EXIT
  .review-venv/bin/python - "$SLURM_JOB_ID" "$benchmark_exit" <<'PY'
import datetime, json, sys
from pathlib import Path
job_id, code = sys.argv[1], int(sys.argv[2])
base = Path('experiments/training_throughput_2026-10-18')
path = base / f'launch_{job_id}.json'
state = json.loads(path.read_text())
output = base / f'job_{job_id}/results.json'
result = json.loads(output.read_text()) if output.exists() else {}
state.update(status=result.get('status', 'failed'), exit_code=code,
             finished_at_pst=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-8))).isoformat())
temporary = path.with_name(path.name + '.worker.tmp')
temporary.write_text(json.dumps(state, indent=2) + '\n')
temporary.replace(path)
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
state = json.loads(path.read_text())
world = int(os.environ['SLURM_GPUS_ON_NODE'])
assert world == state['requested_gpus'] and world in (2, 4, 8)
state.update(status='running', admission_status='released',
             started_at_pst=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-8))).isoformat())
state.pop('hold_reason', None)
temporary = path.with_name(path.name + '.worker.tmp')
temporary.write_text(json.dumps(state, indent=2) + '\n')
temporary.replace(path)
PY

.throughput-venv/bin/python -B -u scripts/benchmark_training_suite.py \
  --world-size "$SLURM_GPUS_ON_NODE" \
  --model-config config/qwen3_4b_throughput_model.json \
  --output-dir "$benchmark_job" \
  --global-batch-sequences 32 --sequence-length 4096 \
  --warmup 3 --steps 8 \
  --profile-runtime-seconds 280 --total-runtime-seconds 1020
