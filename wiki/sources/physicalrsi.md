---
type: source
url: https://mmlab.hk/research/PhysicalRSI
published: unknown
ingested: 2026-10-18
tags: [agentic-robotics]
concepts: [自改进, VLA 当技能调用]
benchmarks: ["[[RoboDojo]]"]
methods: ["[[harness evolution]]", "[[code skills from experience]]", "[[evolutionary code search]]"]
models_used: ["[[π0.5]]"]
models_compared: ["[[π0.5]]", "[[GPT-6 Astra]]", "[[DM0.5]]", "[[Liber-0 Lite]]", "[[Simate-beta]]"]
lenses: ["[[agentic-robotics]]"]
---
# PhysicalRSI 1.0

多模态基座（System 2）用具身反馈反复改写 System 1 的 harness（路由、代码技能、工具、控制代码，π₀.₅ 作为其中一个技能），每轮生成多个变体、按仿真表现选优继承；RoboDojo-Sim 官方总榜第一。

- **关键数字**：
  - RoboDojo-Sim 官方总榜（2026-10-08）：Score 36.27、SR 31.38%，54 个模型第一；第二 Awomo-0.5 35.34，GPT-6-Astra 28.97，GPT-5.5 1.13，DeepSeek-Flash 2.99。
  - solve equation：PhysicalRSI 60%，Astra 40%，π₀.₅ / DM0.5 / Liber-0 Lite / Simate-beta 均 0%；Open 类 Score 28.88，Astra 34.36。
  - fold clothes 演化 4 轮：SR 7.5% → 27.5% → 32.5% → 38%。
  - 52 个 task × layout 设定里 12 个未完成 rollout。
- **评估与接纳**：分数取官方榜单；迭代内 `select_on_eval` 选优，选优用的集合与榜单评测是否不相交未说明；基座模型未说明。
- **可信度**：项目页自报；无论文、无评测次数说明；代码称在 XPolicyLab。
- **模型**：π0.5 是 harness 中的一个技能，System 2 基座未说明；对照取自官方榜单 2026-10-03 快照的 π0.5、GPT-6 Astra、DM0.5、Liber-0 Lite、Simate-beta。
- **原文**：[[raw/physicalrsi]]
