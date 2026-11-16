# Real PEAR evaluation
Status: prepared and statically checked, not executed on a GPU in this project.

## Hypothesis and controls
Test whether the model's success is more stable when a goal or object layout changes than when only wording or appearance changes. Use the released BF16 LIBERO-only checkpoint and base Qwen separately, the same episode configuration, effort, token budget and controller.

A π0.5 or WAM comparison requires its own official adapter and a matched evaluation protocol. This repository does not pretend a hand-written policy is either model.

## Install upstream
Use Linux with the upstream-supported CUDA 13 driver and NVIDIA H100/H200 or GB300. The documented H100 node layout uses eight GPUs, TP=4 and substantial host memory for KV-cache offload. Set node count according to a provisioned cluster; do not interpret ROLLOUT_NNODES=1 as one GPU. Single-5090 NVFP4 deployment is a separate official path and cannot be substituted for the BF16 accuracy experiment.

```bash
git clone https://github.com/mit-han-lab/pear.git
cd pear
git checkout f32aa1f7c2ec9c3f45630cc9f8541b3201e8e087
export WORK_DIR=/absolute/shared/pear-work
bash scripts/install.sh libero_run
bash scripts/install.sh libero_pro
```

Follow the upstream [quick start](https://github.com/mit-han-lab/pear/blob/f32aa1f7c2ec9c3f45630cc9f8541b3201e8e087/docs/getting_started/quickstart.md) to start rollout nodes. Download [LIBERO-only weights](https://huggingface.co/mit-han-lab/Qwen3.8-27B-PEAR-LIBERO_only) and record the actual model revision. Preserve BF16.

## The 80-episode smoke run
The provided config uses 4 suites × 2 tasks × 2 initial states × 5 perturbations = 80 episodes. This tests the pipeline, not the paper's accuracy estimate. It is deliberately a small deterministic prefix; a larger study should predeclare a representative task selection and multiple independent runs.

From this repository:

```bash
export PEAR_ROOT=/absolute/path/pear
export WORK_DIR=/absolute/shared/pear-work
export GPU=h100
export RAY_ADDRESS=<head-ip>:6379
export ROLLOUT_NNODES=<provisioned-rollout-node-count>
export MODEL=/absolute/path/Qwen3.8-27B-PEAR-LIBERO_only
export RUN=/absolute/shared/pear-work/runs/paired-pear-001
bash scripts/run_paired_eval.sh
python3 scripts/summarize_eval.py "$RUN/val_dumps/eval_0.jsonl" --expected 80
```

Repeat with base weights and a different RUN. Never change the task instruction while retaining the original success predicate: the upstream LIBERO-Pro tasks supply the changed goal and corresponding evaluator.

The launcher accepts upstream Hydra overrides. For each run, preserve the resolved Hydra config, model revision, GPU topology, upstream commit, exact episode config, raw JSONL, simulator logs, and per-episode videos if recorded. The JSONL schema was checked against upstream `pear/eval/embodied.py`.

## Larger study
Use all 40 tasks and 50 initial states: 10,000 total episodes including “none”, or 2,000 per perturbation. Report standard and changed-task conditions separately. Match suite/task/trial identifiers from environment metadata; UID alone is not a cross-run pairing key. Estimate uncertainty clustered by task, not just by episode.

Record task success, invalid actions, round count, context exhaustion, end-to-end time and model latency. For a quantization ablation, compare BF16 and NVFP4 on the same episode set and report speed and accuracy together. Do not infer NVFP4 success from BF16 results.

## Why no new result is claimed
This session has no provisioned compatible NVIDIA evaluation cluster. The released model pages also show no hosted inference provider. This repository contains completed data analysis plus a real evaluator launcher; no PEAR model ran locally.

