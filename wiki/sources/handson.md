---
type: source
url: https://github.com/TsinghuaC3I/HandsOn
published: 2026-10-19
ingested: 2026-10-22
tags: []
concepts: [双手灵巧操作仿真基准, 任务验收协议, 泛化迁移评测, 数据采集与重渲染]
benchmarks: []
methods: []
models_used: ["[[π0.5]]", "[[DM0.5]]", "[[LingBot-VLA]]", "[[HY-Embodied-0.5-VLA]]", "[[Spatial Forcing]]", "[[OpenWAM-α]]", "[[Fast-WAM]]", "[[Motus]]", "[[Diffusion Policy]]", "[[GPT-6 Astra]]"]
models_compared: []
lenses: []
---
# HandsOn

基于 Isaac Sim 与 ROKAE–Wuji 双手平台的灵巧操作仿真基准：66 个任务、18,000 条人类演示（约 6.05M 步、30 Hz），分 Core-50 与只用于泛化的 Transfer-16；八个多任务 checkpoint 中最好的 OpenWAM 在 Core-50 任务宏平均成功率 29.1%。

- **关键数字**：
  - Core-50：最好训练策略 OpenWAM 29.1%（每任务 100 回合）；工具使用与精密装配仅 2–3%，推动、关节操作与抓放 35–51%。
  - GPT-6 Astra + move_eef、无 HandsOn 微调：Core-50 26/500（5.2%）、Transfer-16 3/160（1.9%），合计 29/660（4.4%），66 个任务中只有 12 个出现成功。
- **评估与接纳**：作者在 Core-50/Transfer-16 上评 5 个 VLA、3 个 WAM、单任务 DP 与 GPT-6；成功由任务自带谓词判定，checkpoint 预先固定、不按成功率挑选。
- **可信度**：作者自报；环境、协议数据与演示开源，策略 checkpoint 不再分发，端到端复现论文分数需要原 checkpoint 与语言/种子协议。
- **模型**：π0.5、DM0.5、LingBot-VLA、HY-Embodied-0.5-VLA、Spatial Forcing 是 VLA；OpenWAM-α、Fast-WAM、Motus 是 WAM；Diffusion Policy 是单任务基线；GPT-6 Astra 是用 move_eef 接口的提示式控制器。
