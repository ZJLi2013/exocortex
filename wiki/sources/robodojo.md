---
type: source
url: https://robodojo-benchmark.com/
published: 2026-07-06
ingested: 2026-10-18
tags: [agentic-robotics]
concepts: [仿真与真机统一评测, 可复现的远程真机评测, 统一策略接口, 公开排行榜]
benchmarks: []
methods: []
models_used: ["[[π0.5]]", "[[π0]]", "[[GR00T-N1.7]]", "[[SmolVLA]]", "[[GPT-6 Astra]]", "[[GPT-5.5]]"]
models_compared: []
lenses: ["[[agentic-robotics]]"]
---
# RoboDojo

通用机器人操作策略的仿真加真机统一 benchmark：42 个仿真任务、18 个真机任务，公开排行榜另设 agent 赛道；截至 2026-10-17，仿真榜前两名是 agent 赛道的 WorldScape-R²SI（Score 46.58）和 EmbodiedEvo（45.08）。

- **关键数字**：
  - 仿真榜前十（Score / SR）：WorldScape-R²SI 46.58 / 39.35%，EmbodiedEvo 45.08 / 38.95%，VPP2 39.26 / 32.26%，PhysicalRSI 36.27 / 31.38%，其余 30.74–35.34。
  - 首发榜 2026-07-06 收 30 个策略；之后由 RoboDojo 团队加测 GPT-6-Astra 28.97 / 22.48%、GPT-5.5 1.13 / 0.88%。
  - 真机榜只在新闻里见到一条：OpenWAM-α 37.6 / 24.4%。
  - 仿真分五个能力维度：泛化、记忆、精度、长程、开放指令；真机用三种本体（ARX X5、Gemini 305、Piper X）。
- **评估与接纳**：
  - 排行榜由非营利的 AI MMLab Club 维护，称不接受商业资助；多数条目注明由提交方团队贡献，谁跑评测未说明。
  - 仿真在 Isaac Sim 里异构并行；真机由 RoboDojo-RealEval 统一硬件、场景复位、评测协议与部署接口，支持远程 24 小时连续评测。
  - 策略经 XPolicyLab 接一次即可在仿真与真机上评测。
- **可信度**：项目页自报；每任务评测次数只在 DeepSeek-Flash 一条上写明（10 次）；代码开源；论文 arXiv 2607.04434 未收录。
- **模型**：π0.5、π0、GR00T-N1.7、SmolVLA 在首发榜的 30 个策略里，GPT-6 Astra 与 GPT-5.5 由 RoboDojo 团队加测；都是被评测的对象。
- **原文**：[[raw/robodojo]]
