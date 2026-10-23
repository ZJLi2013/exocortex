---
type: lens
tags: []
---
# interactive-video-world-models

## 范围

构建可交互、长程生成的视频世界模型的工作：其数据整理、latent 表示、因果训练与蒸馏方法，以及衡量生成是否跟随控制信号的评测。

## 总结

三个构建工作分别给出数据与训练配方、latent 表示、可在想象中闭环评测策略的动作条件模型；一个 benchmark 拿同一段动作下的预测视频与真机执行比，长回合上各模型分数明显下降。构建类工作没有共同的定量对照：SolarWM 只给定性 rollout，Ctrl-World 的 README 不给数字。全部是自报。

## 工作

- [[solarwm]]：多源视频整理成 1.43M 段帧对齐片段，同一套三阶段配方套在四种 5B–33B 骨干上，蒸馏出 16 fps、4 步采样的因果模型，最长连续生成 60 分钟；只有定性 rollout。（自报）
- [[cadre-autoencoders-and-world-models]]：冻结 DINOv3 特征上训瓶颈、一到两步因果扩散解码的视频自编码器；基于其 latent 的世界模型单张 H100 单用户 20 FPS、输入 p95 162 ms。（自报）
- [[ctrl-world]]：DROID 上训练、基于 Stable Video Diffusion 的动作条件世界模型，让 π0.5-DROID 在想象中闭环 rollout 评测指令遵循；H100 每个 1 秒交互步约 5 s，README 不给评测数字。（自报）
- [[worldoracle]]：同一初始观测与动作轨迹下比预测视频与真机执行，335 条、约 40% 是失败段；WorldOracle-SV 从 30 秒到全长，GE-Sim 2.0 73.86 → 63.33，Cosmos 3 53.99 → 26.60。（自报）
