---
type: source
url: https://github.com/evolvent-ai/RSIGym
published: 2026-10
ingested: 2026-10-16
tags: []
concepts: [选出集合与确认集合分离, 人定义评估与验收, harness 演化, 自改进, 服务化研究预算]
lenses: ["[[agent-loop]]"]
---
# RSIGym

让 research agent 改进另一个系统（数据、harness 或两者）的环境；6 个研究 agent × 5 个领域，30 个 Joint run 有 29 个超过初始系统。

- **关键数字**：
  - RSI-Index（各 benchmark 的 (final − initial) / (1 − initial) 等权平均）0.2079–0.4809，Opus 5 最高；起点 Qwen3.5-35B-A3B-Base + minimal harness，每次 \$500 服务预算。
  - Harness track：Qwen3.6-35B-A3B-Instruct 权重固定，Opus 5 改 DSH，Terminal-Bench 30.34% → 40.82%，三次全对的任务 15 → 26。
  - 自改进：Qwen3.8-27B 同时当研究者和被改进对象，6 题开发集上的增益没有迁移，37 题 SkillsBench 全集 56.66% → 56.26%。
- **评估与接纳**：任务定义（`instruction.md`、`key.json`）规定初始系统、可改部分、提交物、评估协议与事后审计；官方评测 avg@3。
  final evaluation 复用开发期可见的任务。
- **可信度**：作者自报；每个研究配置只跑一次；研究 agent 推理与官方评测不计入 \$500。
- **原文**：[[raw/rsigym]]
