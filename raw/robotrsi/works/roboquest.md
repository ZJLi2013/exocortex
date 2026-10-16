# 主动探索与「自己判断做完了」的评测：RoboQuest

**RoboQuest 是评测场地，不是方法：每个任务都藏着完成所需的信息，移动操作臂必须靠物理交互把它找出来，并按下实体 Submit 键宣布完成。
五个前沿模型零样本最好的是 GPT-6 Astra，23.2%；最常见的失败是没做完就提交。**
[代码](https://github.com/declare-lab/RoboQuest)（MIT），论文 arXiv:2610.10388（declare-lab），示范数据集在 Hugging Face `declare-lab/RoboQuest`。

- **任务**：RoboCasa365 厨房里 10 个移动操作任务，分三族：搜索（锁柜、找物、黑暗中找物）、检查（看不见的面、杯底标签、陌生容器怎么开）、试验（插销顺序、印章图案、垫平桌脚、找重量不同的包裹）。
- **评测**：500 个实例（每任务 50 个），厨房风格留出；成功率在 Submit 时由任务代码判定，另有分阶段的进度分 P。每次决策最多 200 步。
- **接口**：API 模型经 Inspect Robots harness；外部 CLI agent 经 `act.py`；VLA 经 openpi 的 WebSocket。公开的 openpi checkpoint 没见过移动底座与 Submit 键，要先在 PandaOmron 数据上微调。

| 模型（零样本） | 成功率 | 进度 | 每 episode 成本 |
|---|---|---|---|
| GPT-6 Astra | 23.2% | 48.0% | $11.29 |
| Claude Opus 5.5 | 13.8% | 37.3% | $6.83 |
| GPT-6.1 Sol | 12.2% | 34.0% | $1.99 |
| Claude Fable 5.1 | 11.4% | 31.0% | $19.22 |
| Gemini 3.8 Flash | 2.0% | 9.2% | $3.37 |

- 去掉最容易的 Puzzle Box（最好 96%），Astra 降到 15.1%，其余模型都低于 8%；两个搜索任务五个模型 500 个 episode 只解开一次。
- Astra 有 62% 的 episode 提交错误，Opus 5.5 有 49% 直接放弃：瓶颈在判断完成与坚持探索，不只在操作。

对 RobotRSI 判断的影响：

- 它测的是自进化方法普遍没覆盖的一段：收集信息与判断完成。「提交过早」直接支持「接纳权限」轴：谁宣布成功要与谁执行分开。
- 没有学习协议，只能作场地；要测自进化，得自己套 Playground → 冻结 → Test 的流程（EmbodiedEvo 式）。
- 场地是 MuJoCo，但 README 要求 NVIDIA GPU 的 EGL 渲染，AMD 上未验证；单次完整评测约 240 GB 产物。移动操作臂与本目录的 LIBERO 单臂动作空间不同，暂不作底座。

## 可信度

- 数字来自仓库 README 与 `results/eval50/`（核于 2026-10-16），未读论文正文。成本按各家公开单价折算。
