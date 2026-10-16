# 一个场景学到的经验冻结后可跨场景、跨模型复用：EmbodiedEvo

**编码 agent 在每个任务的一个 Playground 场景里把物理反馈蒸馏成代码 Skills 与文本 Lessons，冻结后交给全新的 agent 去做未见过的场景，权重不动。同一个 GPT-6 Astra 在 RoboDojo-Sim 上从官方的 22.48% 提到 37.82%；增益集中在依赖记忆和协调流程的任务，精细接触仍然做不好。**
分级 L3（agent 写 Python 程序调原生 `step(action)`），写回是代码 + 文本。[代码](https://github.com/Einsia/EmbodiedEvo)，论文 [arXiv:2610.18867](https://arxiv.org/abs/2610.18867)（2026-10-13，Einsia / 清华）。

接口只有四个原语：`get_instruction`、`get_observation`、`step(action)`、`reset`，观测是 RGB 与机器人状态，不给物体真值位姿、深度和相机标定。agent 在独立工作区里改 `submission/solution.py` 并提交执行，看录像、日志和剩余预算后决定下一步；Python 变量与机器人状态在两次提交之间保留。

两阶段协议：

- **Playground**：每个任务一个场景，允许 `reset` 重试，agent 可写 `skills/`（如带预算和对准检查的 `pick_from_above`）与 `lessons/`（适用条件、失败模式、恢复办法）；
- **Test**：先冻结 `skills/` 与 `lessons/` 再抽场景，每个场景都是全新的 agent、工作区和模拟器，知识只读、不能 `reset`，也不能跨场景学习。

RoboDojo-Sim 共 42 个任务。dev 集每任务 5 个场景（每个条件 210 个 episode），全集每任务 50 个场景（2,100 个 episode，单 seed）。

| 对照（执行器 Astra/xhigh，场景相同） | Score | SR |
|---|---|---|
| 全集，任务描述 + 官方 wiki：官方 Astra 结果 | — | 22.48% |
| 全集，任务描述 + 官方 wiki：EmbodiedEvo | 44.48 | 37.82% |
| dev 集，只给任务描述：无经验 | 14.77 | 8.50% |
| dev 集，只给任务描述：Skills / Lessons | 38.64 | 30.17% |
| dev 集，只给任务描述：同一 Playground 的原始交互历史 | 36.41 | 29.78% |

- **结构化经验和原始历史效果相当，但便宜一半。** 每个 Test episode 的成本：无经验 $4.06，Skills / Lessons $5.73（+41%），原始历史 $12.20。Playground 的获取成本不计入。
- **强模型的经验能帮弱模型。** Astra 的 Skills / Lessons 让 Sol 与 Luna 的成功率比无经验分别高 8.86 与 5.50 个百分点。
- **零样本 agent 的预算花在摸索操作上。** 这是方法的出发点：Astra 在 tic-tac-toe 里第 367 个动作才第一次抓稳圆环，用掉 1,100 个动作预算的三分之一，最后超时。论文另报告 Playground 里没完成任务的探索也能产出可用的 Skills / Lessons，细节未收入本页。
- **精细插入与倒液体仍失败**，与 RoboProbe「语义强、精密接触弱」一致。

对本页判断的影响：

- 开头的判断多了一份同场地、同执行器的配对证据：经验写成代码与文本、冻结后迁移，权重不动也能大幅提分。
- 它的 Playground → 冻结 → Test 就是本页要求的冻结 release 评测纪律。与 RoboRSI 不同的是，经验只积累一个场景、只读给全新 agent，没有跨版本的持续演化与回滚。
- 接触仍是瓶颈，支持候选问题「接触原语换 VLA」：L3 的代码经验解决了流程与记忆，解决不了精细接触。
- 场地是 RoboDojo（Isaac Sim，需要 NVIDIA GPU），与 RoboProbe 一样，MI300 上基本跑不了；作方法参照，不作 RobotRSI 底座。

## 可信度

EmbodiedEvo 的数字来自 arXiv:2610.18867 的 HTML（2026-10-13）与仓库 README。官方 Astra 22.48% 是 RoboProbe 的结果，不是作者复跑；全集只跑一个 seed；成本按固定单价折算，不含 Playground。仓库是源码导出，未选许可证，集群脚本与结果归档不在内。
