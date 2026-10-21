---
type: source
url: https://research.nvidia.com/labs/srl/projects/astranomy/
published: unknown
ingested: 2026-10-21
tags: [agentic-robotics]
concepts: [前沿模型直接当策略, 动作表示对比, 几何信息写进提示, 推理延迟与成本]
benchmarks: ["[[RoboLab]]"]
methods: []
models_used: ["[[GPT-6 Astra]]", "[[Codex]]", "[[Cosmos3-Nano-Policy]]"]
models_compared: ["[[GPT-6 Sol]]", "[[GPT-6 Luna]]", "[[Claude Opus 5.5]]", "[[Cosmos3-Nano-Policy]]", "[[π0.5]]"]
lenses: ["[[agentic-robotics]]"]
---
# Astranomy

NVIDIA 对 GPT-6 Astra 当原生机器人策略的实证研究，比较直接出动作、在 Codex 会话里出动作、监督 WAM 提案三种用法；RoboLab-120 上 Codex 会话里的 Agentic Policy 成功率 74.8%。

- **关键数字**：
  - RoboLab-120（每任务 5 回合）SR / 完成分：Agentic 74.8% / 83.6（449/600），Orchestrated 66.5% / 79.1，Direct（EEF）66.3% / 76.7；参照 Cosmos3-Nano-Policy 36.8%、π0.5 28.0%（各 1,200 回合），榜单最好的 Lakeside 51.0%。
  - 代价：Direct 每次推理平均 18.56 s；每个成功回合 Agentic 30.9M token / $36.40，Direct 160k / $1.96。
  - 30 任务消融（150 回合）：Direct 下 Astra 72.7%，GPT-6 Sol 33.3%，GPT-6 Luna 2.0%，Claude Opus 5.5 25.3%；EEF 72.7%、关节位置 48.7%、B-spline 37.3%；提示加夹爪与相机几何 19.3% → 72.7%。
- **评估与接纳**：仿真 DROID 场景，RoboLab 自带成功判定与完成分；给出 95% Clopper–Pearson 区间。扩展接口 80.0% → 86.0% 的配对差不显著（McNemar p = 0.108）。
- **可信度**：作者自报；成本按 2026-10-01 价格估算；页面未写发布日期。
- **模型**：GPT-6 Astra 是被研究的策略；Agentic 用 Codex 会话；Orchestrated 由 Astra 审查 Cosmos3-Nano-Policy（DROID 上微调的 WAM）的动作块。π0.5 与 Cosmos3-Nano-Policy 也是参照策略；Sol、Luna、Opus 5.5 是模型消融。
