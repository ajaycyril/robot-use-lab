#!/usr/bin/env bash
set -euo pipefail
LAB_ROOT=$(cd "$(dirname "$0")/.." && pwd)
: "${PEAR_ROOT:?Set PEAR_ROOT to the upstream PEAR checkout}"
: "${WORK_DIR:?Set WORK_DIR to the installed shared PEAR work directory}"
: "${GPU:?Set GPU=h100 or gb300 for the upstream evaluation recipe}"
: "${ROLLOUT_NNODES:?Set the number of rollout nodes already running in Ray}"
: "${MODEL:?Set MODEL to the local BF16 model directory}"
: "${RUN:?Set a fresh absolute output directory}"
PIN=f32aa1f7c2ec9c3f45630cc9f8541b3201e8e087
ACTUAL=$(git -C "$PEAR_ROOT" rev-parse HEAD)
if [[ "$ACTUAL" != "$PIN" ]]; then
  echo "Upstream commit differs from the reviewed version: $PIN" >&2; exit 2
fi
case "$GPU" in h100|gb300) ;; *) echo "Upstream evaluation supports h100/gb300; 5090 server deployment is a separate path." >&2; exit 2;; esac
if [[ -e "$RUN" ]]; then echo "RUN exists; choose a new directory to preserve previous results." >&2; exit 2; fi
export EPISODES="$LAB_ROOT/configs/libero_pro_paired_smoke.json"
export N=1 EVAL_STEP=0
cd "$PEAR_ROOT"
bash examples/eval/eval_libero_pro.sh "$@"

