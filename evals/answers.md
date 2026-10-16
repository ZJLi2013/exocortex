## Q1

把「选出候选」与「确认胜出」分开的有 6 项，另有 3 项被记为反例（`wiki/concepts/选出集合与确认集合分离.md`；agent-loop lens 判断 3，`wiki/lenses/agent-loop.md`）。

分开的：
- **EmbodiedEvo**：Playground 场景学 Skills / Lessons，冻结后在不同布局的 Test 场景评测（每任务 50 个 Test 场景），Test 只读、不能 reset。`wiki/sources/embodiedevo.md`
- **EmbodiedRSI**：每任务 10 个 seed 演化，另 10 个互不相交的 seed 评测，每 seed 10 次试验。`wiki/sources/embodiedrsi.md`
- **ASPIRE**：小 debug split 上学，互不相交的 held-out seed 上报告（LIBERO-Pro 每任务 50、Robosuite 100、BEHAVIOR-1K 25）。`wiki/sources/aspire.md`
- **RAX**：正式评测在从未见过的 held-out 布局上；探索用了哪些布局、seed 数未说明。`wiki/sources/rax.md`
- **AlphaEvolve**：部分分开——Borg 在历史负载快照上选、近期未见负载上确认后才部署；kernel 输入形状对半分训练 / 评估。矩阵乘与数学问题没有独立确认集。`wiki/sources/alphaevolve.md`
- **Agent Laboratory**：仅 MLE-Bench 部分——训练集切 20% dev 集选程序，Kaggle 真实测试集确认。`wiki/sources/agent-laboratory.md`

反例（选出与确认同一集合）：
- **RSIGym**：Qwen3.8-27B 在 6 题开发集上选出的系统，37 题全集 56.66% → 56.26%；官方评测复用开发期可见任务。`wiki/sources/rsigym.md`
- **RSIAgent**：练习与最终评测是同一目标任务，只是环境 reset、memory 冻结。`wiki/sources/rsiagent.md`
- **autoresearch**：保留 / 丢弃与确认用同一个 val_bpb。`wiki/sources/autoresearch.md`

## Q2

Gemini 4 Argon 只有一篇 Google 开发者博客（2026-10-13）与 prompt 演示；模型闭源，经付费 Gemini API / AI Studio 提供（`wiki/sources/gemini-4-argon.md`）。

已知读数（均为博客自报）：
- ERQA 87%（纯推理，不是任务成功率）。
- 仿真造数据：一张真机照片建 MuJoCo 孪生、定义 77 个任务、生成 4,500+ 条 `reward == 1.0` 轨迹微调 VLA；真机成功率 56% → 75%（未给评测次数），完成时间 35 s → 24 s。
- SO-101 硬件自改进三轮耗时 58.9 s → 22.9 s（擦到盒沿）→ 17.4 s；三个阶段与安全规则由人写，提速超过 2× 需人授权。
- 零样本控制按 2–4 / 4–7 / 8–20 次 VLM 调用分档，未给成功率。
- Spot 演示用 foot / hand 两个验证 agent 确认后才释放。`wiki/concepts/验证 agent.md`

在本库里的状态：robotrsi lens 下是待批准草稿（支持判断 3「基座接管建仿真、定义任务、判分、造数据」），未并入当前判断（`wiki/lenses/robotrsi.md`）；agent-loop lens 判为 reject（`wiki/log.md`）。

## Q3

`wiki/concepts/人定义评估与验收.md` 列了 11 个来源；agent-loop lens 判断 1 把它概括为「能稳定涨分的 research agent 都跑在它改不了的评估协议、预算和事后审计之内」（`wiki/lenses/agent-loop.md`）。

- **RSIGym**：`instruction.md` 与 `key.json` 规定初始系统、可改部分、提交物、评估协议（avg@3）、\$500 服务预算与事后审计。`wiki/sources/rsigym.md`
- **autoresearch**：评估写死在人写、不可改的 `prepare.py`，每次固定 5 分钟；agent 只改 `train.py`，人改 `program.md`。`wiki/sources/autoresearch.md`
- **AlphaEvolve**：评估函数 `evaluate` 由用户写；只适用于能写出自动评估器的问题，部分结果由人类专家确认正确性。`wiki/sources/alphaevolve.md`
- **EmbodiedEvo**：协议文件与执行记录对 agent 只读，Test 阶段不能 reset。`wiki/sources/embodiedevo.md`
- **EmbodiedRSI**：VLA 冻结，成功用 benchmark 二值结果，消融时 VLA、任务集、实验预算与评估协议固定；判定器由谁实现未说明。`wiki/sources/embodiedrsi.md`
- **ASPIRE**：环境、原语 API 与评估协议固定，agent 只能调用预定义原语；成功由谁判定未说明。`wiki/sources/aspire.md`
- **RAX**：操作员 arm / disarm 目录 agent 不可写，recorder 只读，只能经 MCP 工具碰机器人。`wiki/sources/rax.md`
- **RSIAgent**：官方评估器在所有循环之后调用、不回传分数；但练习期的接纳由 verifier agent 判，不是人。`wiki/sources/rsiagent.md`
- **Gemini 4 Argon**：硬件自改进三阶段与安全规则由人写，提速超过 2× 要人授权。`wiki/sources/gemini-4-argon.md`
- **RoboQuest**：成功由 benchmark 规则在 SUBMIT 时判定，隐藏信息 agent 读不到（它是评测前沿模型的 benchmark，agent 不做自改进搜索）。`wiki/sources/roboquest.md`
- **Agent Laboratory**：只算部分——人给研究想法、最终质量靠人评；流程内接纳由 LLM 评审定，自动评审比人评高约 2.3 分（6.1 vs 3.8）。`wiki/sources/agent-laboratory.md`

## Q4

按来源页 `published` 字段，2026-10 发布的有 4 项：
- **Gemini 4 Argon**：2026-10-13。`wiki/sources/gemini-4-argon.md`
- **EmbodiedEvo**：2026-10（arXiv 2610.18867）。`wiki/sources/embodiedevo.md`
- **EmbodiedRSI**：2026-10（arXiv 2610.10498）。`wiki/sources/embodiedrsi.md`
- **RoboQuest**：2026-10（arXiv 2610.10388）。`wiki/sources/roboquest.md`

可能但来源页未确认：
- **RSIGym**：来源页 `published: unknown`（`wiki/sources/rsigym.md`）；原文 README 链接的论文是 arXiv 2610.10310，按 arXiv 编号是 2026-10 提交（`raw/rsigym.md`）。
- **RAX**：只写到年份 2026，月份查不到。`wiki/sources/rax.md`

不是 2026-10：RSIAgent 2026-09、autoresearch 2026-03、AlphaEvolve 2025-06、Agent Laboratory 2025-01；ASPIRE 页面无日期，BibTeX 引 arXiv:2607.00272（`wiki/sources/aspire.md`）；ScienceDiscovery 为 unknown（`wiki/sources/sciencediscovery.md`）。

## Q5

自改进没迁移或被当反例的记录集中在 agent-loop lens 与三个来源：

- **RSIGym**：Qwen3.8-27B 同时当研究者和被改进对象，6 题开发集上的增益没迁移，37 题 SkillsBench 全集 56.66% → 56.26%。`wiki/sources/rsigym.md`、`wiki/concepts/自改进.md`、`wiki/concepts/选出集合与确认集合分离.md`
- **agent-loop lens**：判断 2「在小开发集上自己挑候选的自改进没有迁移到全集」；判断 4「本库没有固定 benchmark，维持不做自改进」；判断 6 把 autoresearch 的贪心接受规则当反例。`wiki/lenses/agent-loop.md`
- **autoresearch**：val_bpb 变好即保留，选出与确认同一指标，是贪心接受的反例来源。`wiki/sources/autoresearch.md`
- **RSIAgent**：选出与确认是同一目标任务（反例）；只 DRS 在 T085、T089 低于 baseline，四题消融只 DRS 56.50% vs 完整 74.54%；verifier 在官方 rubric 下仍误判 PASS，未验证的决定被写成规则复用，练习没覆盖目标的真正弱点；Play2Code 在最强生成器上 52.77 → 51.05。`wiki/sources/rsiagent.md`、`wiki/concepts/经验写成代码技能.md`
- **AlphaEvolve**：优化了 Gemini 训练 kernel（训练时间减 1%），但改进下一版 AlphaEvolve 的反馈环以月计、增益温和。`wiki/sources/alphaevolve.md`
- **EmbodiedRSI**：真机 5 任务中 Glasses Bridge Grasp 一项下降 60.0% → 56.7%。`wiki/sources/embodiedrsi.md`
