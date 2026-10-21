---
type: source
url: https://github.com/OpenSenseNova/SenseNova-RoboRSI
published: 2026-10-09
ingested: 2026-10-19
tags: [agentic-robotics]
concepts: [自改进, VLA 当技能调用]
benchmarks: ["[[RoboDojo]]", "[[LIBERO-Pro]]", "[[RoboCasa365]]"]
methods: ["[[harness evolution]]", "[[execution trace training]]", "[[retest before release]]"]
models_used: ["[[GPT-6 Astra]]", "[[Qwen3.8-27B]]", "[[sensenova-roborsi]]"]
models_compared: ["[[GPT-6 Astra]]", "[[Simate-beta]]", "[[Qwen3.8-27B]]"]
lenses: ["[[agentic-robotics]]"]
---
# SenseNova-RoboRSI

共享运行时接模型、技能与机器人工具；用执行 trace 改 Harness、模型权重不动，验证过的改动进入下一版。RoboDojo-Sim 平均分 60.08、成功率 54.17%。

- **关键数字**：
  - RoboDojo-Sim（SenseNova-RoboRSI / GPT-6 Astra）：平均分 60.08、成功率 54.17%；相对 GPT-6 Astra 基线 28.97 / 22.48% 高 31.11 分、31.69 个百分点。正在提交官方榜，称官方结果可能略有出入。参考榜更新于 2026-10-14、访问于 2026-10-15。
  - LIBERO-Pro：94.50%。文中 RPent 对照来自 Task/Swap；官方 LIBERO-PRO 榜是五种扰动的另一套合计。
  - RoboCasa365：Target kitchens + task memory（Target50）64.60%。官方条目用 pretraining kitchens，作者称不能据此排名。
  - 27B-Preview（开源权重预计 2026-10-20）：RoboDojo 平均分 26.13、任务成功率 20.83%（VLA 辅助），比 RoboDojo 团队评的 GPT-6 Astra 低 2.84 分。LIBERO-Pro：VLA 辅助 95.0%，直接 VLM 控制 96.1%。RoboCasa365：相对 Qwen3.8-27B 26.0% → 46.5%，平均输出 token 59.5K → 15.9K（−73.3%）。
- **评估与接纳**：候选改动在相同任务条件下复测，验证通过才带入下一版。谁实现评分、评测次数未说明。真机有演示，无成功率。
- **可信度**：作者自报；RoboDojo 分数尚未上官方榜；27B 权重与技术报告未发布；未给评测次数。
- **模型**：Harness 结果的底座是 GPT-6 Astra。27B-Preview 把验证过的交互经验变成多模态监督，基座是 Qwen3.8-27B。对照点名 GPT-6 Astra、Simate-beta、Qwen3.8-27B。

## 关联

- 对照 [[embodiedevo]]：RoboDojo-Sim 同表 EmbodiedEvo 平均分 45.08、成功率 38.95%，本文 60.08 / 54.17%
- 对照 [[physicalrsi]]：同表 PhysicalRSI 36.27 / 31.38%
