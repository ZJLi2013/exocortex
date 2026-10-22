---
type: source
url: https://github.com/rootyJeon/VPM
published: 2026-10-20
ingested: 2026-10-22
tags: []
concepts: [多视角视频与点轨迹联合预测, 点轨迹监督动作学习, 相机条件多视角生成, 轨迹经逆运动学转动作]
benchmarks: ["[[LIBERO]]", "[[LIBERO-Plus]]", "[[RoboCasa]]", "[[VP-WorldBench]]", "[[ReCamMaster]]", "[[CMU Panoptic]]", "[[PointMotionBench]]"]
methods: []
models_used: ["[[Cosmos 3 Nano]]"]
models_compared: ["[[π0.5]]", "[[GR00T-N1.5]]", "[[GR00T-N1.7]]", "[[Cosmos 3 Nano]]", "[[DreamZero]]"]
lenses: []
---
# VPM

在多视角视频历史与语言指令下联合预测未来多视角视频与持久 3D 点轨迹的世界模型，并把机器人动作作为 token 模态一起去噪；点轨迹监督同时提高视频预测与操作成功率。

- **关键数字**：
  - 真机 DROID 三个 pick-and-place 任务各 24 次：Banana 79.2%、Cup 70.8%、Cube 54.2%；无点监督的 VPM (V+A) 为 58.3 / 64.6 / 43.8，Cosmos3-Nano 为 50.0 / 54.2 / 41.7。
  - 仿真三视角：LIBERO 97.2%、LIBERO-Plus 84.6%、RoboCasa 76.2%（Cosmos3-Nano 依次 96.8 / 81.6 / 72.0）。
  - VP-WorldBench 仿真机器人子集：FVD 67.35 对 VPM (V) 78.52、Cosmos3-Nano 104.74；δ3D 50.05 对 43.62 / 39.03。
- **评估与接纳**：作者自评；仿真按各 benchmark 标准协议、统一三视角，真机每任务 24 次；成功判定方式原文未说明。
- **可信度**：自报；单个 checkpoint（VPM-DROID），真机只测三个任务；代码与权重开源，权重为 CC BY-NC 4.0。
- **模型**：Cosmos 3 Nano 是底座，分三阶段训练；π0.5、GR00T-N1.5、GR00T-N1.7、DreamZero 是对照的 VLA / 世界动作模型。
