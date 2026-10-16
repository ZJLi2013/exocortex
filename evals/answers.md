# answers

## Q1

把「选出候选的集合」和「确认胜出的集合」分开的工作：

- **EmbodiedRSI**：进化用 10 个 seed，评测用另外 10 个 seed，两者不相交；代码与技能只在同一批初始状态上测出正的联合增益才留下。`raw/robotrsi/works/embodiedrsi.md`、`raw/robotrsi/landscape.md`
- **EmbodiedEvo**：每个任务在一个 Playground 场景里学，先冻结 `skills/` 与 `lessons/` 再抽 Test 场景；Test 只读，不能 `reset`，也不能跨场景学习。`raw/robotrsi/works/embodiedevo.md`
- **RAX**：用冻结的程序在留出布局上评测；技能要两次无人值守成功才标 `verified`。`raw/robotrsi/works/rax.md`
- **ASPIRE**：debug seed 与 held-out seed 分开。`raw/robotrsi/landscape.md`
- **Zetta**：用 held-out，另做历史失败回归。`raw/robotrsi/landscape.md`
- **SHAPER**：用固定的 validation episodes 做接纳。`raw/robotrsi/landscape.md`
- **agent-loop（探索模式）**：把它定为要求：确认胜出分支所用的集合不能是选出它的集合；提升时注明选出胜者的集合，确认用另一组或更大的集合。这条要求的来由是反例 RSIGym：它的自改进用 6 题开发集选出 checkpoint，在 37 题全集上不涨。`raw/agent_loop/research-rsi-track.md`
- 不分开的工作：**PhyAgentOS** 成功次数够了就晋升，不留出 seed。`raw/robotrsi/works/phyagentos.md`

## Q2

- **公开状态**：只有 Google Developers Blog（2026-10-13）上的 prompt 与演示视频说明，没有论文或技术报告。模型闭源，走付费 API（Gemini API 付费档与 AI Studio），版本无法冻结。评测次数、成本、延迟都没公开。`raw/robotrsi/works/gemini-argon.md`、`raw/robotrsi/landscape.md`
- **已知读数**：
  - ERQA 87%：纯推理题的分数，不是任务成功率。`raw/robotrsi/works/gemini-argon.md`
  - 仿真造数据：一张照片建出 MuJoCo 孪生，定义 77 个任务，生成 4,500+ 条 `reward == 1.0` 的轨迹去微调 VLA；真机成功率 56% → 75%，完成时间 35 s → 24 s，没给评测次数。`raw/robotrsi/works/gemini-argon.md`、`raw/robotrsi/landscape.md`
  - SO-101 硬件自改进：三轮各跑一次，耗时 58.9 s、22.9 s（擦到盒沿）、17.4 s。`raw/robotrsi/works/gemini-argon.md`
  - 零样本控制：没有成功率；最细一档是 8–20 次调用的视觉伺服。`raw/robotrsi/works/gemini-argon.md`

## Q3

由 human 写评估器、任务定义或验收，agent 只在其内搜索的系统：

- **AlphaEvolve**：评估器是用户提供的程序化评估器，人写评估器。`raw/agent_loop/research-rsi-track.md`
- **RSIGym**：人写任务定义（`instruction.md`、`key.json` 锁 base model 与 \$500 预算）并做事后审计；评估器是固定的 benchmark 子集。`raw/agent_loop/research-rsi-track.md`
- **GEPA**：用户给定评估，人定义目标。`raw/agent_loop/research-rsi-track.md`
- **autoresearch**：`val_bpb` 按约定只读，人维护 `program.md`。`raw/agent_loop/research-rsi-track.md`
- **Gemini 4 Argon 的 SO-101 硬件自改进**：三个阶段、安全规则（`AGENTS.md`）与验收由人写，模型在其内读日志、改程序、重试。`raw/robotrsi/works/gemini-argon.md`、`raw/robotrsi/landscape.md`
- **ENPIRE**：先固定 reset / reward，再自动做实验。笔记没写 reset / reward 由谁固定。`raw/robotrsi/landscape.md`
- **agent-loop 自身**：固定评估、预算上限，持久改动由人批准。`raw/agent_loop/research-rsi-track.md`

## Q4

2026-10-13 及以后读过或核过的工作：

- **RSIGym**：2026-10-16 读，读了 README、任务定义和 rsi-index.ai。`raw/agent_loop/research-rsi-track.md`
- **ScienceDiscovery**：2026-10-16 读，读了 README 和开发者文档；它的 evolution sidecar 页面在 2026-10-16 核查时 404。`raw/agent_loop/research-rsi-track.md`
- **RAX**：README 核于 2026-10-16。`raw/robotrsi/works/rax.md`、`raw/robotrsi/landscape.md`
- **PhyAgentOS**：README 核于 2026-10-16。`raw/robotrsi/works/phyagentos.md`、`raw/robotrsi/landscape.md`
- **RoboQuest**：README 与 `results/eval50/` 核于 2026-10-16。`raw/robotrsi/works/roboquest.md`
- **EmbodiedEvo**：依据 2026-10-13 的 arXiv HTML 与仓库 README；landscape 记的公开状态日期是 2026-10-13。`raw/robotrsi/works/embodiedevo.md`、`raw/robotrsi/landscape.md`
- **Gemini 4 Argon**：依据 2026-10-13 的博客；landscape 记的公开状态日期是 2026-10-13。`raw/robotrsi/works/gemini-argon.md`、`raw/robotrsi/landscape.md`

EmbodiedEvo 和 Gemini 4 Argon 笔记里的 2026-10-13 是来源发布日期。landscape 说带链接的几项「公开状态核于各自笔记的日期」，所以算作核于该日。

## Q5

记录自改进没迁移、或被当作反例的地方：

- **RSIGym 的自改进**：Qwen3.8-27B 同时当研究者和被改进对象，用 6 题开发集选出的 checkpoint，在 37 题全集上从 56.66% 降到 56.26%。这被写进当前判断：「在小开发集上自己挑候选的自改进没有迁移到全集」。`raw/agent_loop/research-rsi-track.md`
- **RSIGym 的 Harness track**：涨分只证明有固定 benchmark 时自改 harness 有效；本库没有这类 benchmark，所以维持「不做自改进」。`raw/agent_loop/research-rsi-track.md`
- **autoresearch**：它的贪心接受规则被当作反例。`raw/agent_loop/research-rsi-track.md`
- **Agent Laboratory**：它「难以引导」被当作反例依据，用来支持 human 在时间盒末介入。`raw/agent_loop/research-rsi-track.md`
- **RSIAgent**：在数字环境里 memory-only 自进化有效，具身迁移性未验证。`raw/robotrsi/landscape.md`
- **RoboRSI**：RAX 那种随探索量递增的曲线，RoboRSI 在本目录没复现出来。`raw/robotrsi/works/rax.md`
- **EmbodiedRSI 的局部回退**：harness 从仿真迁到真机后，抓眼镜鼻梁从 60.0% 降到 56.7%，其余任务都上升。`raw/robotrsi/works/embodiedrsi.md`
