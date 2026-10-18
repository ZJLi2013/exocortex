## Q1

把选出与确认分开的工作（`wiki/lenses/agent-loop.md` 判断 3 是这一条原则本身）：

- **EmbodiedEvo**：Playground 与 Test 布局不同；Playground 可 reset、可写经验，Test 只读、不能 reset、不回写；RoboDojo-Sim 成功率 37.82%。`wiki/sources/embodiedevo.md`
- **EmbodiedRSI**：每任务 10 个 seed 演化，在另外 10 个互不相交的 seed 上评测（每 seed 10 次）；RoboCasa365 77.0%。`wiki/sources/embodiedrsi.md`
- **ASPIRE**：小 debug split 上学，互不相交的 held-out seed 上报告（LIBERO-Pro 每任务 50、Robosuite 100、BEHAVIOR-1K 25）。`wiki/sources/aspire.md`
- **RAX**：正式评测用从未见过的 held-out 布局；探索在哪些布局上、seed 数未说明。`wiki/sources/rax.md`
- **AlphaEvolve**：只有 Borg（历史快照选出、未见近期负载确认）和 kernel（输入形状一半训练、一半评估）分开；矩阵乘与数学问题没有独立确认集。`wiki/sources/alphaevolve.md`
- **Agent Laboratory**：仅 MLE-Bench 部分，在训练集切出的 20% dev 集选程序，再上 Kaggle 真实测试集确认。`wiki/sources/agent-laboratory.md`
- **JevAny**：choice-token blend 权重在开发数据上调好后冻结再评测。`wiki/sources/jevany.md`

未分开（选出与确认同一集合）：RSIGym（final evaluation 复用开发期任务）`wiki/sources/rsigym.md`、RSIAgent（练习与最终评测是同一目标任务）`wiki/sources/rsiagent.md`、autoresearch（同一 val_bpb）`wiki/sources/autoresearch.md`、AlphaNIST（只有训练成功率，无 held-out）`wiki/sources/alphanist.md`。

## Q2

- **公开状态**：2026-10-13 的 Google 开发者博客；只有博客与 prompt 演示；模型闭源，经付费 Gemini API / AI Studio 提供。`wiki/sources/gemini-4-argon.md`
- **已知读数**：ERQA 87%（纯推理，不是任务成功率）；一张照片建 MuJoCo 孪生、定义 77 个任务、生成 4,500+ 条 `reward == 1.0` 轨迹微调 VLA，真机成功率 56% → 75%（未给评测次数），完成时间 35 s → 24 s；SO-101 硬件自改进三轮 58.9 s → 22.9 s → 17.4 s；零样本控制只按 VLM 调用次数分档，未给成功率。`wiki/sources/gemini-4-argon.md`
- **wiki 内状态**：robotrsi 判断 3 的支持草稿仍在「待批准」，未并入当前判断 `wiki/lenses/robotrsi.md`；agent-loop 判 reject `wiki/log.md`。

## Q3

- **AlphaEvolve**：评估函数 `evaluate` 由用户写，LLM 只对用户标记的代码块提 diff。`wiki/sources/alphaevolve.md`
- **autoresearch**：评估写死在人写、不可修改的 `prepare.py`，agent 只改 `train.py`，每次固定 5 分钟。`wiki/sources/autoresearch.md`
- **RSIGym**：任务定义（`instruction.md`、`key.json`）规定可改部分、提交物、评估协议与事后审计，每次 \$500 服务预算。`wiki/sources/rsigym.md`
- **EmbodiedEvo**：协议文件与执行记录对 agent 只读。`wiki/sources/embodiedevo.md`
- **RAX**：agent 只能经 MCP 工具碰机器人，操作员 arm / disarm 目录不可写，recorder 只读。`wiki/sources/rax.md`
- **ASPIRE**：评估协议、机器人编程 API 与原语集合固定。`wiki/sources/aspire.md`
- **EmbodiedRSI**：成功为 benchmark 二值结果，VLA 冻结，评估协议固定。`wiki/sources/embodiedrsi.md`
- **RSIAgent**：最终分由 benchmark 官方评估器在循环之后给出、不回传；选题规则与报告口径由作者定。`wiki/sources/rsiagent.md`
- **Gemini 4 Argon**：硬件自改进的三个阶段由人写，安全规则来自 `AGENTS.md`，提速超过 2× 需人授权。`wiki/sources/gemini-4-argon.md`
- **Agent Laboratory**（部分）：人给研究想法、co-pilot 在子任务末设人工检查点；流程内接纳仍由 LLM 打分。`wiki/sources/agent-laboratory.md`
- **RoboQuest**（benchmark 而非搜索系统）：成功由 benchmark 规则判定，隐藏信息放在 agent 读不到的私有 specification。`wiki/sources/roboquest.md`

总判断见 `wiki/lenses/agent-loop.md` 判断 1：能稳定涨分的 research agent 都跑在它改不了的评估协议、服务预算和事后审计之内。

## Q4

`published` 为 2026-10 的来源：

- **Gemini 4 Argon**（2026-10-13）`wiki/sources/gemini-4-argon.md`
- **RoboQuest**（2026-10）`wiki/sources/roboquest.md`
- **EmbodiedEvo**（2026-10）`wiki/sources/embodiedevo.md`
- **EmbodiedRSI**（2026-10）`wiki/sources/embodiedrsi.md`
- **SGS**（2026-10）`wiki/sources/sgs.md`

不确定：**RSIGym** 来源页写 `unknown`，但其原文链了自己的 arXiv 2610.10310，按收录规则应为 2026-10 `wiki/sources/rsigym.md`。RAX 只写 2026 `wiki/sources/rax.md`；AlphaNIST、JevAny、OpenJev、ScienceDiscovery 为 unknown；ASPIRE 为 unknown，BibTeX 引 arXiv:2607.00272（即 2026-07，非 10 月）`wiki/sources/aspire.md`。

## Q5

- **RSIGym**：Qwen3.8-27B 同时当研究者与被改进对象，6 题开发集上的增益没迁移，37 题 SkillsBench 全集 56.66% → 56.26%。`wiki/sources/rsigym.md`；对应 `wiki/lenses/agent-loop.md` 判断 2、4。
- **autoresearch**：val_bpb 变好即保留的贪心接受规则被列为反例（判断 6）。`wiki/sources/autoresearch.md`、`wiki/lenses/agent-loop.md`
- **RSIAgent**：作为判断 3 的反例草稿——练习与最终评测同一目标任务；verifier 在官方 rubric 下误判 PASS，未验证的决定被写成规则复用；只 DRS 在 T085、T089 低于 baseline；Play2Code 在最强生成器上 52.77 → 51.05。`wiki/sources/rsiagent.md`、`wiki/lenses/agent-loop.md`
- **Agent Laboratory**：「难以引导」是只在时间盒末介入的反例（判断 7）；co-pilot 的研究者评分（实验质量 2.38、有用性 3.75）低于自主模式。`wiki/sources/agent-laboratory.md`、`wiki/lenses/agent-loop.md`
- **AlphaEvolve**：改进下一版 AlphaEvolve 的反馈环以月计、增益温和。`wiki/sources/alphaevolve.md`
- **EmbodiedRSI**：仿真演化的 harness 零样本上真机，Glasses Bridge Grasp 一项下降 60.0% → 56.7%。`wiki/sources/embodiedrsi.md`
