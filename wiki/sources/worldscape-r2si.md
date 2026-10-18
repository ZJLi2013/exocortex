---
type: source
url: https://feng.ifeng.com/c/8xIuPhHNWQl
published: 2026-10-17
ingested: 2026-10-18
tags: [agentic-robotics]
concepts: [自改进, 执行记录训练动作模型, 更新先过测试再发布]
benchmarks: ["[[RoboDojo]]"]
methods: ["[[harness 演化]]", "[[经验写成代码技能]]"]
models_used: ["[[WorldScape Policy]]"]
models_compared: ["[[GPT-6 Astra]]", "[[GR00T-N1.7]]"]
lenses: ["[[agentic-robotics]]"]
---
# WorldScape R²SI

Manifold AI 的双层 agent：内层 Robot Agent 按任务加载 Skill 执行（调用 reactive model WSP 也是一种 Skill），外层 Recursion Agent 复盘执行记录、修订 Skill，并用执行记录训练 WSP；称 RoboDojo 总榜第一。

- **关键数字**：
  - push_T（不用 WSP）：首轮 723 步超 600 步预算；修订 Skill 后 596 步原生满分，再迭代到 389 步（约 −35%）；冻结后 3 个随机布局 222 / 312 / 256 步，均满分。
  - 称 RoboDojo 总榜第一、超过 GPT-6-Astra 与 GR00T-N1.7，未给总分与成功率。
- **评估与接纳**：更新须通过测试才自动发布并纳入版本管理；测试内容与谁判定未说明。push_T 修订在同一布局上做，冻结后在随机布局上报告。
- **可信度**：公司发布稿（机器之心转载）；无论文；单任务单次案例；外层用哪个模型未说明。
- **模型**：动作模型是 WorldScape Policy；称 RoboDojo 上超过 GPT-6-Astra 与 GR00T-N1.7。
- **原文**：[[raw/worldscape-r2si]]
