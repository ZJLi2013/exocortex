---
type: source
url: https://github.com/HorizonRobotics/IGGT4D
published: 2026-07-21
ingested: 2026-10-22
tags: []
concepts: [流式 4D 重建, 实例接地的几何预测, 在线实例码本聚类, 几何引导实例标注]
benchmarks: ["[[HiRoom]]", "[[ETH3D]]", "[[7Scenes]]", "[[ScanNet++]]", "[[HOI4D]]", "[[Waymo]]", "[[PointOdyssey]]"]
methods: []
models_used: []
models_compared: []
lenses: []
---
# IGGT4D

流式实例接地的几何 Transformer，逐帧增量更新相机位姿、深度与实例特征，在长动态视频上同时做 3D 重建与实例跟踪；长序列实例跟踪平均 T-mIoU 58.84 / T-SR 85.41，IGGT 在同样设置下显存不足。

- **关键数字**：
  - 长序列（约 100 帧，HOI4D 40 帧）实例空间跟踪平均：T-mIoU 58.84、T-SR 85.41；SAM2 45.38 / 58.65，SpaTrackerV2+SAM 43.73 / 59.28，IGGT OOM。
  - 3D 重建（无真值位姿）平均 F1 0.6678，流式基线最好 LingBot-Map 0.5228；离线 DA3 0.7430。
  - 开放词表语义分割长序列平均 mIoU 40.08 / mAcc 73.84，LSeg 31.95 / 48.23。
- **评估与接纳**：作者自评，在 HiRoom、ETH3D、7Scenes、ScanNet++、HOI4D、Waymo、PointOdyssey 上按各自指标比较，未由第三方复评。
- **可信度**：自报；推理代码与 checkpoint 已开源，数据集 InsScene4D-147K、训练代码、benchmark 与评测代码尚未发布。
