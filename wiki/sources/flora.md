---
type: source
url: https://research.nvidia.com/labs/gear/flora/
published: unknown
ingested: 2026-10-21
tags: [agentic-3d]
concepts: [时间戳动作描述, 过程奖励标注, 结果奖励标注, 替代 API 模型做数据标注]
benchmarks: ["[[WGO-Bench]]", "[[RoboReward]]", "[[Robometer]]", "[[DenseCaptionBench]]", "[[DenseRewardBench]]", "[[RubricBench]]"]
methods: []
models_used: []
models_compared: ["[[GPT-6 Astra]]", "[[GPT-5.6 Sol]]", "[[Claude Opus 5]]", "[[Kimi-K3]]"]
lenses: []
---
# Flora

NVIDIA 训练 GR00T 用的开源数据引擎模型，给人与机器人操作视频标时间戳描述、过程奖励与结果奖励；RoboReward MAE 40.0（GPT-6 Astra 55.4），成本约为 GPT-6 Astra 的 1/125。

- **关键数字**：
  - 奖励：RoboReward MAE 40.0（Astra 55.4）；DenseRewardBench 失败召回 53.3（Astra 0.0）；Robometer OOD Kendall 72.0（Astra 82.3）。
  - 描述：DenseCaptionBench Human100 联合 F1 37.4（Astra 29.7）；Robot200 51.0（Astra 57.9）；WGO-Bench 联合语义 F1 34.5（Astra 39.0）。
  - RubricBench pooled L1 误差 6.5（Astra 3.6）。
  - 生产规模：512 张 GB300 每天标 200,000 小时数据。
- **评估与接纳**：项目页一张表，对照四个前沿模型；摘要称 WGO-Bench、RoboReward、Robometer 上 SOTA，在「内部 benchmark」上与 Astra 相当，未说明哪几个是内部集。
- **可信度**：作者自报；模型放在 Hugging Face；评测次数未说明；页面未写发布日期。
- **模型**：Flora 本身是被评测的标注模型，底座未说明；产出的标注用于训练 GR00T，版本未说明。对照 GPT-6 Astra、GPT-5.6 Sol、Claude Opus 5、Kimi K3。
