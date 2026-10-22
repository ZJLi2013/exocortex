---
type: source
url: https://github.com/Bench2Dex/Bench2Dex
published: 2026-09-14
ingested: 2026-10-22
tags: []
concepts: [共享仿真触觉接口, 跨具身双手灵巧操作, 不变性与等变性泛化轴, 稳定成功与阶段完成率]
benchmarks: ["[[Bench2Dex]]"]
methods: []
models_used: ["[[ACT]]", "[[Diffusion Policy]]", "[[π0.5]]", "[[GR00T-N1.5]]"]
models_compared: []
lenses: []
---
# Bench2Dex

12 种灵巧手、26 个双手操作任务的仿真视触觉 benchmark，用统一的接触几何触觉接口和约 1.3K 条遥操作示范评测四类策略；四通道平均稳定成功率 GR00T N1.5 最高 28.3%，π0.5 20.3%、ACT 18.0%、Diffusion Policy 7.1%。

- **关键数字**：
  - 每个任务-具身-策略在 None / Equi. / Inv. / Full 四个泛化通道各 50 次 rollout；四通道平均 SR：GR00T N1.5 28.3%、π0.5 20.3%、ACT 18.0%、DP 7.1%；LSCR 依次 47.3 / 36.1 / 33.5 / 23.0%。
  - 无扰动 None：GR00T N1.5 48.5%、ACT 29.5%、π0.5 27.3%、DP 12.9%；Full 同时扰动：GR00T 19.8%、π0.5 19.7%、ACT 13.0%、DP 3.8%。
  - 26 个任务、12 种具身、约 1.3K 条示范、8 类观测模态；7 种扰动分为不变性轴（5 种）与等变性轴（2 种）。
- **评估与接纳**：作者自己跑四个策略；成功用可达-停止（reach-and-stop）稳定判定，终止条件需保持 0.5 秒，另报阶段完成率 LSCR；固定任务级随机种子。
- **可信度**：自报；只在仿真里评，触觉接口未与任何实体传感器校准；代码、数据与 checkpoint 开源。
- **模型**：ACT 与 Diffusion Policy 从零训练，π0.5 与 GR00T N1.5 从预训练 checkpoint 全量微调，四者都是被评测对象。
