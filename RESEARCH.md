# Source review
Reviewed 16 November 2026.

## All four links in the original post
Original: https://x.com/jmtang42/status/2121304157952860379

| Link | What was inspected | What it establishes |
|---|---|---|
| [Blog](https://mit-han-lab.github.io/pear-blog/) | Method, comparisons, transfer, effort, quantization, limitations and appendix tables | The authors' headline results and their qualifications |
| [Paper](https://mit-han-lab.github.io/pear-blog/paper.pdf) | Main claims and protocol; appendices B–H, including full RoboDojo, trial-level failures and prompts | Sample sizes, historical baseline provenance, difficult-task failures and action semantics |
| [Code](https://github.com/mit-han-lab/pear) | Installation, evaluation scripts, model settings, deployment, LIBERO-Pro environment and evaluation record format | Concrete reproduction path; Linux/CUDA and multi-GPU evaluation requirements |
| [Weights](https://huggingface.co/collections/mit-han-lab/pear) | All three checkpoints and their file/type metadata | BF16 final, BF16 LIBERO-only, and NVFP4 deployment variants; no hosted inference provider shown |

Reviewed upstream commit: `f32aa1f7c2ec9c3f45630cc9f8541b3201e8e087`.

## Distinctions that change the interpretation
- RURL is the training method; PEAR is the infrastructure. The model starts from Qwen3.8-27B, then learns with robot-use reinforcement learning.
- No demonstrations means none in this robot-use RL procedure. It does not establish that the foundation model's pretraining contained no relevant visual or robotic information.
- The model outputs changes to end-effector pose and gripper quantities in textual JSON. Inverse kinematics and a controller still execute motion. It is not direct torque control.
- The 74.4% LIBERO and perturbation results use the LIBERO-only checkpoint. The 18/30 real result uses the later LIBERO + RoboDojo checkpoint.
- The real robot was unseen, but the later checkpoint practiced the corresponding task types in simulation.
- The π0.5 aggregate comes from prior sources. Differences can reflect training distribution, objective, model, budget and protocol, not architecture alone.
- Standard LIBERO and the “none” condition inside LIBERO-Pro are not interchangeable. The paper's Table 4 gives a different all-five-conditions aggregate (64.5%) from the four-perturbation mean (62.1%).
- RoboLab comparisons in the paper use an October 29 leaderboard snapshot. The live leaderboard has newer policies. A 37.3 vs 36.8 point estimate does not establish statistical superiority.
- “No measurable degradation” on nine selected benchmarks is not proof of equivalence or preserved ability on every task.
- Decode speed uses NVFP4, DFlash2 and specialized engines. Evaluation success uses BF16. The authors report a quantization accuracy penalty and longer reasoning.
- Published videos shorten pauses and change playback speed. They are not real-time latency evidence.

## Actual completed experiment
`analysis.py` independently recomputes arithmetic from transcribed source results. The 30 real-robot rows come from Table 7. Each repeated scene/object has two trials; Wilson intervals are a descriptive independent-trial approximation, not a deployment guarantee.

A hypothetical mixture of standard LIBERO and changed-goal tasks gives a crossover near 28.4% changed goals. This is a sensitivity calculation over source aggregates. It neither represents a sampled deployment workload nor controls training and compute.

All trial failures remain visible: 6 round-budget failures, 3 unaligned outcomes, 2 toppled objects, 1 rolled-away ball. Comparing trial keys, the later checkpoint gains 13 successes and loses 2 relative to LIBERO-only.

Full RoboDojo: 21/540 is 3.89% micro success. The paper's 5.5% is a macro average across five capability dimensions. 370/540 episodes exhaust context. Do not interchange these measures.

## Context sources
- [π0.5 paper](https://arxiv.org/abs/2504.16054): heterogeneous co-training and generalization, not merely replaying demonstrations.
- [DreamZero / WAM paper](https://arxiv.org/abs/2602.15922): joint video/action modeling and generalization from a pretrained video backbone.
- [RoboLab live leaderboard](https://research.nvidia.com/labs/srl/projects/robolab/leaderboard.html): inspected for current context; the lab visualizes the paper snapshot, not a live ranking.

## Visual provenance
The GIF and PNG charts are original renderings of reported numeric data. They show no fabricated robot motion. Original real-robot replays remain on the [authors' project page](https://mit-han-lab.github.io/pear-blog/).

