# agent × 具身：相关工作地图

**最快的适应环正在移到模型外部：失败先被写成 memory，再固化成可执行、可测试的代码，稳定且高频的行为才蒸馏回权重。**
权重训练没有消失，它从唯一的改进手段变成了慢环。通用多模态基座正在接过这条环里原本由人做的环节：建仿真、定义任务、判分、造数据（[Gemini 4 Argon](works/gemini-argon.md)）。

本页只做地图：比较轴、评测场地、方法与框架各一张表，每项一行，细节在 [`works/`](works/) 的逐篇笔记里。
RobotRSI 自己的判断（RoboRSI 的局限与改进方向、选底座、候选研究问题）在 [direction](direction.md)。

## 四个比较轴

- **分级 = 谁输出动作**，沿用 [LLM-as-Policy](https://arxiv.org/abs/2609.24170) / RoboProbe 的定义：L1 学习得到的 VLA 直接出动作；
  L2 LLM 编排冻结 VLA；L3 LLM 经固定 harness 直接出动作。
- **写回 = 学到的东西存在哪**：无 / memory（经验文本、轨迹骨架）/ 代码（技能与原语本身）/ 权重（执行策略被训练）。
  「agent 改技能代码」是写回轴上的一格，不是新的分级。
- **闭环频率**：action chunk 级 critic（Zetta）、episode 内重试（Harness VLA、RACaP、PhyAgentOS）、episode 间改程序（ASPIRE、SHAPER、HarnessPAI、EmbodiedRSI、EmbodiedEvo、RAX）、
  跨版本发布与回滚（RoboRSI、RegenHarness）。
- **接纳权限**：谁提出改动与谁有权宣布成功必须分开。强门禁要求环境原生谓词或独立 verifier、held-out seeds、历史回归和版本化回滚。

这四个轴用来比较方法与框架；评测场地另按「测什么、能不能在 MI300 上跑」比较。

## agent 介入机器人的四类方式

| 类 | 分级 | 写回 | 代表 | 已知的事 |
|---|---|---|---|---|
| agent 当 policy | L3 | 无 | AGP、Inspect Robots、RoboProbe、Gemini 4 Argon（零样本控制） | 语义判断与纠错强，精密插入弱：Inspect Robots 上 block into bowl 19/20、puzzle into groove 2/20。AGP 接 YAM 单臂，block construction 100% / 100% / 80%，每次成功 20.6–54.3 分钟、$7.46–27.41。Argon 的控制演示走固定原语加验证 agent，没给成功率 |
| agent 编排冻结 VLA | L2 | memory | Harness VLA / RPent、GPT-as-Policy、PhyAgentOS | VLA 权重不动，Harness VLA 把它收成可重试的接触原语，LIBERO-PRO 50.0% → 82.4%。GPT-as-Policy 让 GPT-6 Astra 审查 π0.5 每一步：成功率 48%（Astra 直接控制 26%），只纠正 14.4% 的执行步 |
| agent 改 skill | L3 → L1 | 代码 + 权重 | RoboRSI、ASPIRE、HarnessPAI、EmbodiedEvo、RAX | RoboRSI 代码固化开 / 关 174/600 对 129/600，VLM 调用 −27%、token −29%。RAX 探索 4 → 128 个 episode，留出场景成功率 25% → 79% |
| agent 造环境与数据 | agent 不出动作；训出的 VLA 出动作（L1） | 仿真孪生 + 任务 + 数据 → 权重 | Gemini 4 Argon；RoboRSI 的 zeroshot 数据引擎 | Argon 从一张真机照片建 MuJoCo 孪生、定义 77 个任务、生成 4,500+ 条轨迹微调 VLA，真机成功率 56% → 75%、完成时间 35 s → 24 s，未给评测次数 |

GPT-as-Policy 约 85% 的昂贵审查结论是「继续」，样本小，但给「快判断器过滤无需纠正的步」提供了外部参照。

## 评测场地

| 场地 | 测什么 | 规模 | 公开的最好读数 | MI300 |
|---|---|---|---|---|
| RoboProbe / RoboDojo-Sim | LLM 直接或编排控制，逐格排行榜 | 42 任务 × 50 场景 = 2,100 回合 | GPT-6 Astra 22.48%；[EmbodiedEvo](works/embodiedevo.md) 37.82% | Isaac Sim，基本跑不了 |
| LIBERO-PRO | 指令改写、物体换位等扰动下的单臂操作 | 本目录用 12 任务 × 2 seed；RoboRSI 官方 120 任务 | [EmbodiedRSI](works/embodiedrsi.md) 86.8%（只评 T、S 两类）；Harness VLA 82.4%（自报） | MuJoCo，本目录已跑通 |
| RoboCasa365 | 厨房原子 / 组合任务，含未见组合 | Atomic / Composite × Seen / Unseen | EmbodiedRSI overall 77.0 | MuJoCo，未在本地跑 |
| RoboTwin | 双臂 | — | PhyAgentOS 80.0%（10 任务抽样）；Harness VLA C2R 58.4% | 未在本地跑 |
| [RoboQuest](works/roboquest.md) | 靠物理交互收集隐藏信息，自己按 Submit 宣布完成 | 10 任务 × 50 实例，厨房风格留出 | GPT-6 Astra 23.2%，零样本 | MuJoCo，README 要求 NVIDIA EGL；未验证 |

LIBERO-10 已被 PhyAgentOS 报到 100%，区分不了方法，不列入。

## 方法与框架

| 工作 | 类型 | 主要写回 | 部署时高层 LLM | 接纳机制 | 公开状态 |
|---|---|---|---|---|---|
| Harness VLA / RPent | 方法 + 框架 | memory | 是 | 环境评分器；固定技能库 | 代码公开 |
| RoboRSI | 框架 | 技能代码 + 数据 + 权重 | 是 | 技能测试、git commit、冻结 eval | 代码与脚本公开；项目权重 / 数据未公开 |
| [PhyAgentOS](works/phyagentos.md) | 框架 | 带版本的 Skills + scoped Lessons | 是 | 验证过的成功 episode 数到阈值（默认 3）才晋升 | 2026-10-09：v1.1.0，MIT，技术报告 |
| [EmbodiedRSI](works/embodiedrsi.md) | 方法 | 代码 + 技能 + 分层 memory（VLA 冻结） | 进化期是 | 同初始状态配对；正的联合增益才留边；进化 seed 与评测 seed 不相交 | 2026-10-12：arXiv 与项目页；正文未给代码 |
| [EmbodiedEvo](works/embodiedevo.md) | 方法 | 代码 Skills + 文本 Lessons | 是 | Playground 一个场景学，冻结后才抽 Test 场景；Test 只读、不能 reset | 2026-10-13：arXiv 与源码导出；未选许可证；需 RoboDojo / Isaac Sim 与 NVIDIA GPU |
| [RAX](works/rax.md) | 方法 + 框架 | 编译出的控制程序 + memory + 跨 session 技能库 | 否（程序替代 agent） | 冻结程序在留出布局上评测；技能两次无人值守成功才 `verified` | 2026-10-16：代码分支与技能库公开；Preprint；仿真需 Isaac Sim |
| SHAPER | 方法 | 文本技能 + context-code harness | 是 | 固定 validation episodes | 论文公开；未找到官方代码 |
| ASPIRE | 方法 | 控制程序 + 可复用技能库 | 视场景而定 | debug / held-out seeds 分离 | 代码、技能库与脚本公开 |
| Zetta | 方法 | runtime critic + recovery + 配置 | 否 | 历史失败回归、held-out、版本化 memory | 代码与评测脚本公开 |
| HarnessPAI | 方法 | 任务程序 + repair-skill graph；另蒸馏权重 | 否 | 全批验证后原子 promotion | 论文与项目页公开；未找到官方代码 |
| RACaP | 方法 | typed Policy API + ReAct harness + memory；另蒸馏权重 | 是 | parent / child 配对 promotion | 论文公开；未找到官方代码 |
| RegenHarness | 协议 | context、routing、recovery policy | 可选 | 身份 / 版本绑定 commit gate、回滚 | 协议与案例公开；未找到官方代码 |
| ENPIRE | 方法 | 策略 / 训练代码 + 权重 | rollout 内否 | 固定 reset / reward 后自动实验 | 环境、learner 与 autoresearch 脚本公开 |
| [Gemini 4 Argon](works/gemini-argon.md) | 基座模型 | 控制程序（硬件自改进）；仿真数据 → VLA 权重 | 控制演示里是 | 仿真 `reward == 1.0` 过滤；硬件上由人写阶段与验收 | 2026-10-13：博客与付费 API；模型闭源 |

带链接的几项公开状态核于各自笔记的日期，其余核于 2026-09-29。HarnessPAI 最完整地提出「演化期用 agent，部署期把 agent 编译掉」，RAX 给出了公开实现。
PhysicalCoding 仓库只有报告与素材；PhysicalRSI 项目链接在核查时不可访问；Simate AutoResearch 只有媒体报道。三者都不能作为已有实现参与比较。

## 可信度边界

逐篇工作的口径在各自笔记的「可信度」一节。其余：

- GPT-as-Policy / RoboDojo 的 π0.5 + Astra 读数（48%、均分 62.60、14.4%）来自中文媒体转述，未核对原始报告。
- RoboRSI 项目页正文未抓取成功，描述依据其 README、`docs/` 与 GitHub 元数据（Apache-2.0，2026-08 建仓）。
- RSIAgent 证明的是数字环境里 memory-only 自进化有效（OSWorld 2.0 78.98 vs GPT-6 Astra 72.60），具身迁移性未验证。

## 引用

- [RoboRSI](https://github.com/nssmd/RoboRSI) · [blog](https://lab.noematrix.ai/blog/2-roborsi-research-preview/)
- [EmbodiedRSI](https://arxiv.org/abs/2610.10498) · [项目页](https://geeksongs.github.io/agentic_robotics/)
- [EmbodiedEvo](https://arxiv.org/abs/2610.18867) · [code](https://github.com/Einsia/EmbodiedEvo) · [项目页](https://lab.einsia.ai/embodiedevo)
- [RAX](https://github.com/robot-agent-exploration/rax) · [项目页](https://robot-agent-exploration.com/) · [skills-lib](https://github.com/robot-agent-exploration/skills-lib)
- [PhyAgentOS](https://github.com/PhyAgentOS/PhyAgentOS-core) · [技术报告](https://arxiv.org/abs/2607.16636)
- [RoboQuest](https://github.com/declare-lab/RoboQuest) · [论文](https://arxiv.org/abs/2610.10388)
- [Gemini 4 Argon for Robotics](https://developers.googleblog.com/gemini-4-argon-for-robotics/)
- [RoboProbe](https://github.com/RoboProbe/RoboProbe) · [LLM-as-Policy](https://arxiv.org/abs/2609.24170)
- [RPent](https://github.com/RLinf/RPent) · [Harness VLA](https://arxiv.org/abs/2607.08448)（[项目页](https://harnessvla.github.io/)）
- [GPT-as-Policy](https://github.com/anonymous-report-421/GPT-as-Policy) · [GPT-6 Astra on robot arms](https://openai.robocurve.org/gpt-6-astra/)
- [Agent as Policy (AGP)](https://arxiv.org/html/2609.12541v1) · [RSIAgent](https://arxiv.org/html/2609.15364v1)
- [Zetta](https://air-embodied-brain.github.io/zetta/)（[code](https://github.com/air-embodied-brain/zetta-embodiment)）
- [ASPIRE](https://research.nvidia.com/labs/gear/aspire/)（[code](https://github.com/NVlabs/ASPIRE)） · [ENPIRE](https://research.nvidia.com/labs/gear/enpire/)（[code](https://github.com/NVlabs/ENPIRE)）
- [HarnessPAI](https://darwin-agent.github.io/HarnessPAI/) · [PhysicalCoding](https://github.com/HexaFuture/PhysicalCoding) · [PhysicalRSI](https://mmlab.hk/research/PhysicalRSI)
- [RoboICL](https://github.com/Mosi-AI/RoboICL/tree/main) · [SoL-Pi](https://github.com/NVlabs/SoL-Pi) · [Show-Harness](https://showlab.github.io/Show-Harness/)
- [awesome-astra-embodied-ai](https://github.com/zjwzcx/Awesome-Astra-Embodied-AI) · [llm-robotics-playground](https://github.com/dimentary/llm-robotics-playground)
- [Uranus: next-generation simulation infra for embodied AI](https://d-robotics-ai-lab.github.io/large-model-team/blog/uranus/)
