# 试次用来区分假设：EmbodiedRSI

**一次物理试次按「能区分哪几条代码或技能假设、再除以成本」来排；代码和技能只有在同一批初始状态上测出正的联合增益，才一起留下。VLA 权重全程冻结。**
分级是 L2，写回是代码、技能和分层 memory。[项目页](https://geeksongs.github.io/agentic_robotics/)，论文 [arXiv:2610.10498](https://arxiv.org/abs/2610.10498)（2026-10-07）。项目页与论文正文都没有代码链接。

Fast System 维护假设图。节点是一条代码假设或一条技能假设，有向 `refines` 边指向更具体的修订。每条假设共享同一个 Beta 先验，置信度是后验均值 `(n_sup + α) / (n_sup + n_ref + α + β)`。实验自己声明能更新的假设子集；得分是探索熵的期望下降除以成本（耗时、仿真步数、GPU、reset）。熵或得分低于阈值、预算用尽、或每条假设打到次数上限，这一轮探索停止。

联合增益 `w = R(code, skill) − max(R(code), R(skill))`。配对试验固定初始状态，以及其余调用和它们的顺序。`w > 0` 时 Slow System 在图上记一条双向 `works-with` 边。

Slow System 把证据分成三层：M1 是原始 episode（轨迹、调用的工具、VLA 被调用的时刻、动作、遥测、结果、奖励），M2 是假设图，M3 是从重复证据蒸馏出的可复用认知。Manager 在 Retain、Merge、Abstract、Compress、Forget、Skip 里选一条，用 PPO 训练。奖励在下一次物理实验之后结算：任务成功率的变化，加上探索熵的下降，再减去那次实验的成本。执行这条 memory 动作的是冻结的 Qwen3.5-122B-A10B，嵌入用 Qwen3-Embedding-0.6B。M1 原文和 M2 的证据计数保持不动，改的是检索索引或 M3。Fast System 生成假设用的模型，正文没有点名。

仿真评测是每任务 10 个 seed、每个 seed 10 次；进化用另外 10 个 seed，与评测不相交。仿真里的 VLA 骨干写在附录，主文没有点名。

RoboCasa365（%）。Composite-Unseen 是 71.3 对 Harness VLA 的 40.1；总分是 77.0 对 63.6。

| | Atomic-Seen | Composite-Seen | Composite-Unseen | Overall |
|---|---|---|---|---|
| EmbodiedRSI | 94.4 | 63.1 | 71.3 | 77.0 |
| Harness VLA（该文表） | 91.3 | 55.8 | 40.1 | 63.6 |

LIBERO-Pro 只评指令改写（T）和物体换位（S），总分 86.8，Harness VLA 72.1，Zetta 71.1。相对 Harness VLA 八格都更高，缺口最大的是换位：Spat-S 93 对 69，LIBERO-10-S 71 对 49。Zetta 只报了 GOAL 和 LIBERO-10；这四格里它只在 Goal-T 更高，92.5 对 78.0。

真机是 SO-101。SmolVLA 先按任务用 50 条遥操作、在 4×H200 上训 20k step，然后冻结；从仿真迁过去的是 harness。每任务 30 次，总分从 46.0% 到 71.3%。扑克筹码（面值 ×5 = 100）从 10.0% 到 90.0%。眼镜鼻梁抓取从 60.0% 到 56.7%。

| 任务 | SmolVLA | EmbodiedRSI |
|---|---|---|
| Oreo 放进红碗 | 70.0% | 86.7% |
| 扑克筹码（×5=100） | 10.0% | 90.0% |
| 两块蛋糕叠到午餐肉罐头上 | 63.3% | 76.7% |
| 抓眼镜鼻梁 | 60.0% | 56.7% |
| 叠衣服 | 26.7% | 46.7% |
| 总分 | 46.0% | 71.3% |

消融是论文自报。Composite-Unseen 上联合演化 71.3%，只演化技能 55.6%；只演化代码在 Atomic-Seen 上高于只演化技能，到 Composite-Unseen 次序反过来，只演化代码的那一格正文没有给出数字。50 个物理 episode 后的 overall 是 72.9% 对随机探索 27.1%（学习 AUC 0.635 对 0.309），正文没有点名这个 overall 属于哪个 suite。另一条 LIBERO-Pro SPAT-T 曲线里，按信息价值选实验在第 48 个 episode 把 8-episode 滚动成功率拉到 100% 并保持；随机选择到第 100 个 episode 仍在波动，结束时约 75%。memory 动作的选择：检索 61.7%、PPO 只用任务奖励 65.2%、完整奖励 71.3%（Composite-Unseen；AUC 0.556 / 0.589 / 0.635）。

- 候选问题「memory vs code」有了一份外部消融：联合高于任一单改，两种单改谁更高随 suite 翻转。协议是他们的，不是本目录的冻结 release。
- 每轮都在生成新的代码假设和技能假设。本页改进方向把新增原语当成少见、人审、升版本的事件。
- 上表 Harness VLA 的 72.1%（LIBERO-Pro）和 63.6%（RoboCasa overall）来自 EmbodiedRSI 的协议。本页前面引用的 LIBERO-PRO 82.4%、RoboCasa365 55.4% 来自 Harness VLA 论文自己的数字。

## 可信度

EmbodiedRSI 的数字来自 arXiv:2610.10498 的 HTML（2026-10-07）与项目页。附录里的仿真骨干、信息价值权重和 PPO 超参未收入本页。未找到代码仓库。
