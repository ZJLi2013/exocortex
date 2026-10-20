---
type: source
url: https://4dcodebench.com/
published: 2026-10
ingested: 2026-10-19
tags: [agentic-3d]
concepts: [代码重建动态场景, 逆图形学评测, 运动写成曲线而非仿真]
benchmarks: []
methods: []
models_used: []
models_compared: ["[[GPT-6 Astra]]"]
lenses: ["[[agentic-3d]]"]
---
# 4DCodeBench

编码 agent 只看视频，从零写可执行图形程序，重建动态场景的几何、运动和渲染；18 个 agent、200 个任务。

- **关键数字**：100 段真实视频加 100 段仿真视频。项目页称外观和静态几何普遍好于运动；多数解把运动写成手调曲线，很少建仿真。GPT-6 Astra 领先总排名，推理力度升高时更常做仿真、运动重建更好。未给出总分数字。
- **评估与接纳**：项目页排行榜。每个模型跑一次与否未说明。
- **可信度**：作者自报；项目页。
- **模型**：点名领先的是 GPT-6 Astra。其余对照模型未逐一列出。
- **原文**：[[raw/4dcodebench]]
