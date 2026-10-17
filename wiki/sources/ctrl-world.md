---
type: source
url: https://github.com/Robert-gyj/Ctrl-World
published: 2025-10
ingested: 2026-10-16
tags: []
concepts: [世界模型内策略评测, 世界模型合成轨迹, 世界模型后训练]
lenses: ["[[robotrsi]]"]
---
# Ctrl-World

在 DROID 上训练的动作条件生成式世界模型（基于 Stable Video Diffusion），让 VLA 策略在想象中闭环 rollout，用来评测并改进指令遵循；README 不给评测数字。

- **关键数字**：
  - README 未给成功率，也未给世界模型评测与真机结果的一致性。
  - 训练数据 DROID 约 95k 条轨迹、564 个场景；训练用 1–2 个节点、每节点 8 张 A100 / H100。
  - 每个交互步（1 秒动作块）A100 约 10 s、H100 约 5 s。
  - 论文中每类任务跑 20 次：5 或 10 个初始配置 × 重复 4 或 2 次。
- **评估与接纳**：
  - π0.5-DROID 与 Ctrl-World 都零样本迁到 DROID 开源数据之外的新场景；任务含 pickplace、towel_fold、wipe_table、tissue、close_laptop、stack。
  - 想象 rollout 里的成功由谁判定未说明。
  - 作者声明：能评测指令遵循，但物理交互建模可能不准；接触丰富与可变形物体任务需在下游任务上后训练世界模型（VLAW）。
- **可信度**：ICLR 2026；代码与 checkpoint 开源；数字在论文 arXiv 2510.10125，README 只给用法。
- **原文**：[[raw/ctrl-world]]
