---
type: source
url: https://github.com/google-research/harness2
published: 2026-10
ingested: 2026-10-18
tags: [agent-loop]
concepts: [自改进, 无真值反馈的对比式改进, 跨任务积累改进经验]
benchmarks: ["[[WorkBuddy-Bench]]", "[[JobBench]]", "[[LAB]]"]
methods: ["[[harness evolution]]"]
models_used: ["[[GLM-5]]", "[[Gemini 3.5 Flash]]"]
models_compared: []
lenses: ["[[agent-loop]]"]
---
# Harness²

模型权重不变，在当前任务上提出 harness 改动、试跑、按执行之间的行为对比合成新 harness，再把采纳的 harness 与经验带到后续任务；单步就让 GLM-5 与 Gemini 3.5 Flash 在 WorkBuddy-Bench 上最多涨 11.5 分。

- **关键数字**：
  - 三个专业 benchmark、四种模型–harness 配置下，一步 Propose–Probe–Compose 的最大提升：WorkBuddy-Bench +11.5 分、JobBench +4.5 分、LAB partial pass rate +11.8 个百分点。
  - 加大任务级递归预算（`--k`）称有进一步提升，README 未给数字。
- **评估与接纳**：
  - 任务级：harness editor 提出通用与领域两类改动，在同一任务上试跑，composer 按执行之间的对比合成最终 harness，不用真值反馈。选出与确认是同一任务。
  - 跨任务级：experience reflector 把采纳的 harness 和有证据支持的经验写进持久的 improvement harness。
  - 最终分由各 benchmark 的评判脚本（`harness2-judge`）给；可改的部件有 system prompt、guardrails、memory、tool guidance、subagents、skills、scripts、plugins 八类。
  - README 提醒执行器联网不受限，公开 rubric 可能被查到，需自行配置网络限制。
- **可信度**：作者自报；README 未给评测次数；代码开源（Apache 2.0）；论文 arXiv 2610.14224 未收录。
- **模型**：GLM-5 与 Gemini 3.5 Flash 是被改进 harness 的底座；执行器是 OpenCode 或 Codex，其底层模型未说明。
