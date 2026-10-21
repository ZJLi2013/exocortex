---
type: source
url: https://github.com/NVlabs/SoL-Pi
published: 2026-09
ingested: 2026-10-21
tags: [agent-loop]
concepts: [选出集合与确认集合分离, 人定义评估与验收, token 效率]
benchmarks: ["[[EdgeBench]]", "[[Terminal-Bench]]", "[[IMO]]"]
methods: ["[[harness evolution]]"]
models_used: ["[[GPT-5.6 Sol]]", "[[Claude Opus 5]]", "[[GPT-5.6 Luna]]"]
models_compared: ["[[Codex]]", "[[Claude Code]]"]
lenses: ["[[agent-loop]]"]
---
# SoL-Pi

research agent 读 coding agent 的执行 trace、提 harness 改动，按事先固定的能力与效率门槛筛选，留下四个机制做成 Pi 扩展；EdgeBench 上 token 流量比 Pi 少 44.7–49.0%，API 成本约少三分之一。

- **关键数字**：
  - EdgeBench（51 个公开任务，11 个用于冻结后验收、40 个做最终评测）：完整四机制在 GPT-5.6 Sol 下 1.10 B token，比 Pi 少 49.0%，成本少 33.2%，平均分 42.0 对 Pi 44.8；只开 ObservationPack 时 47.2。
  - 成本相对原生 harness：GPT-5.6 Sol 下比 Codex 低 50.0%，Opus 5 下比 Claude Code 低 54.3%。
  - Terminal-Bench 4（63 个 CPU 任务）：SoL-Pi 解 15 个，Codex、Pi 各 18 个；总成本比 Pi 低 26.3%。
  - IMO 2026（Lean 4 验证）：6 题过 3 题，每题 $20.90，Codex $22.89、Pi $25.32。
  - 搜索规模：152 个方向、535 个可执行环境、3,000 多次运行。
- **评估与接纳**：能力指标、容差与效率指标在搜索前固定，optimizer 不能改；候选须能力在容差内、至少一个效率指标变好。EdgeBench 留作冻结后评测，结果不回流搜索。
- **可信度**：作者自报；EdgeBench 评测次数未说明；kernel 优化实验每种配置跑一次两小时；代码 MIT 开源，论文 arXiv 2609.20519。
- **模型**：GPT-5.6 Sol 与 Opus 5 是主 agent 底座；GPT-5.6 Luna 是 Evidence-Preserving Reducer 的摘录模型；对照 Codex 与 Claude Code 两个原生 harness。research agent 的模型未说明。

## 关联

- 基于 [[autoresearch]]：每条独立搜索沿用 autoresearch 的提出、实现、跑固定实验、保留或丢弃循环，再加实现与评审的迭代。
