---
type: source
url: https://github.com/facebookresearch/robo_jepa
published: 2026-10-07
ingested: 2026-10-21
tags: []
concepts: [世界模型规模律, 目标图像隐空间规划, 多具身数据混合训练]
benchmarks: ["[[RoboCasa]]"]
methods: []
models_used: ["[[V-JEPA 2.1]]"]
models_compared: ["[[π0-FAST]]", "[[π0.5]]"]
lenses: []
---
# RoboJEPA

在冻结 V-JEPA 2.1 编码器的隐空间里训练的动作条件世界模型，22M 到 8B 参数，数据来自 12 种具身的 23 个公开数据集；预测误差随训练算力服从二阶幂律，按单张目标图像做隐空间规划，零样本控制真机 Franka。

- **关键数字**：
  - 真机 Franka 成功率（%）：RoboJEPA-8B 抓取 67、举起 50、拾放 27；π0.5 为 5、0、53；π0-FAST 为 22、12、40（自报，论文 Table 3）。
  - RoboCasa 推物体任务：训练算力约 10²² FLOPs 以下的模型成功率都是 0，之后各尺寸都开始成功（自报）。
  - 两个平台上规划评测超过 50,000 回合（自报）。
- **评估与接纳**：作者自己在 RoboCasa 仿真与 DROID 平台真机上评；离线指标是 DROID 与 RoboCasa 留出集上的隐空间 ℓ1 误差。论文写明 VLA 用文本指令、RoboJEPA 用目标图像，VLA 结果只作参照、不算直接可比的基线。
- **可信度**：作者自报；全部 checkpoint 与训练、部署代码开源（CC BY-NC-SA 4.0）；论文 arXiv 2610.10515。
- **模型**：V-JEPA 2.1 ViT-G/384 是冻结的编码器；π0-FAST 与 π0.5 是真机上的参照策略，经 DROID 微调。
