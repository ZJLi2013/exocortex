---
type: source
url: https://physicalvision.github.io/artisan/
published: 2026-10
ingested: 2026-10-19
tags: [agentic-3d]
concepts: [设计编码审查分工, 物理碰撞验收, 铰接资产生成]
benchmarks: ["[[Artisan-Benchmark]]"]
methods: []
models_used: ["[[GPT-6 Astra]]"]
models_compared: ["[[Claude Fable 5.1]]", "[[Codex]]"]
lenses: ["[[agentic-3d]]"]
---
# Artisan

设计、编码、审查多智能体加物理验证，从文本和可选参考图生成可动的铰接 3D 资产；GPT-6 Astra 配置下单关节碰撞率 1.7%。

- **关键数字**：单关节碰撞率相对 Articulate-Anything 从 31.2% 降到 1.7%；静止稳定性相对 Codex 从 86% 升到 98%；首选偏好相对 Codex 从 21.1% 升到 43.3%。物理分用 Artisan（GPT-6 Astra）。双关节碰撞 3.7%，多关节 13.0%。
- **评估与接纳**：项目页排名表，13 个受评配置；碰撞用物理检查标出错误运动。评测次数未说明。
- **可信度**：作者自报；项目页；默认 GPT-6 Astra、high reasoning、每例 15 美元预算。
- **模型**：GPT-6 Astra 是默认生成 agent。对照 Claude Fable 5.1（单关节碰撞 39.9%）和 Codex。
- **原文**：[[raw/artisan]]
