---
type: concept
---
# harness 演化

模型权重不动，改进围绕模型的执行代码、技能与经验。

## 来源
- [[rsigym]]：Harness track 固定 Qwen3.6 权重，改 DSH，Terminal-Bench 30.34% → 40.82%。
- [[embodiedevo]]：Skills + Lessons 构成 harness，冻结后交给新 agent 与其它模型复用。
- [[embodiedrsi]]：冻结 VLA 外的 harness 联合演化代码与技能，真机 46.0% → 71.3%。
- [[aspire]]：从执行 trace 修 code-as-policy 程序，修复存进技能库。
- [[rsiagent]]：经验写进 actor 自管的 memory，冻结后用于目标任务，不改权重。
- [[autoresearch]]：agent 改训练代码 `train.py`，人改指令 `program.md`。
