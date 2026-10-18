# log

## [2026-10-16] ingest | RSIGym
agent-loop keep；agentic-robotics reject（不涉及机器人）。

## [2026-10-16] ingest | EmbodiedEvo
agentic-robotics keep；agent-loop keep。

## [2026-10-16] ingest | Gemini 4 Argon
agentic-robotics keep；agent-loop reject（硬件自改进的阶段由人写，不是 research agent）。

## [2026-10-16] ingest | ScienceDiscovery
agentic-robotics reject（不涉及机器人）；agent-loop reject（只有产品功能描述，无评估或结果）。

## [2026-10-16] ingest | autoresearch
agent-loop keep；agentic-robotics reject（LLM 训练，不涉及机器人）。

## [2026-10-16] ingest | RAX
agentic-robotics keep；agent-loop keep。

## [2026-10-16] ingest | AlphaEvolve
agent-loop keep；agentic-robotics reject（不涉及机器人）。

## [2026-10-16] ingest | Agent Laboratory
agent-loop keep；agentic-robotics reject（不涉及机器人）。

## [2026-10-16] ingest | RSIAgent
agent-loop keep；agentic-robotics reject（软件环境，不涉及机器人）。

## [2026-10-16] ingest | EmbodiedRSI
agentic-robotics keep；agent-loop keep。

## [2026-10-16] ingest | RoboQuest
agentic-robotics keep；agent-loop reject（评测前沿模型当单回合机器人策略，不是 research agent）。

## [2026-10-16] ingest | ASPIRE
agentic-robotics keep；agent-loop keep。

## [2026-10-16] lint | 新建概念页
经验写成代码技能、跨模型迁移、验证 agent、进化式代码搜索（ASPIRE 的「程序进化搜索」并入）。

## [2026-10-16] query | Q1
concepts/选出集合与确认集合分离、lenses/agent-loop，及 embodiedevo、embodiedrsi、aspire、rax、alphaevolve、agent-laboratory、rsigym、rsiagent、autoresearch 来源页。

## [2026-10-16] query | Q2
sources/gemini-4-argon、concepts/验证 agent、lenses/agentic-robotics、log。

## [2026-10-16] query | Q3
concepts/人定义评估与验收、lenses/agent-loop，及该概念页列出的 11 个来源页。

## [2026-10-16] query | Q4
全部 12 个来源页的 published 字段；RSIGym、RAX 另查 raw/rsigym、raw/rax。

## [2026-10-16] query | Q5
concepts/自改进、concepts/选出集合与确认集合分离、lenses/agent-loop，及 rsigym、rsiagent、autoresearch、alphaevolve、embodiedrsi 来源页。

## [2026-10-16] ingest | JevAny
agentic-robotics reject（机器人只在 playground 回放，无机器人结果）；agent-loop reject（决策模型基础设施，不是 research agent 或自改进系统）。

## [2026-10-16] ingest | OpenJev
agentic-robotics reject（不涉及机器人）；agent-loop reject（决策推理服务器，不是 research agent 或自改进系统）。

## [2026-10-16] ingest | SGS
agentic-robotics reject（纯 RL 训练课程，无 agent）；agent-loop reject（不是 research agent 或自改进系统）。

## [2026-10-16] ingest | AlphaNIST
agentic-robotics reject（纯 RL 训练，无 agent，只有训练成功率）；agent-loop reject（不是 research agent 或自改进系统）。

## [2026-10-16] ingest | Ctrl-World
agentic-robotics keep；agent-loop reject（README 只有世界模型推理与训练，无 agent 循环）。

## [2026-10-16] ingest | Batch-Invariant VLAs
agentic-robotics reject（VLA 推理数值工程，无 agent，不改选底座、改进方向或评测选择）；agent-loop reject（不涉及 research agent）。

## [2026-10-16] lint | lenses
robotics-rl：sgs、alphanist
jev：jevany、openjev

## [2026-10-16] approve lens | robotics-rl
human 批准。keep：sgs、alphanist。
reject：jevany、openjev、batch-invariant-vlas、sciencediscovery、ctrl-world、roboquest、gemini-4-argon、embodiedevo、embodiedrsi、aspire、rax（编码 / 世界模型 / 基座评测，不是无示教 RL 训练课程）；rsigym、autoresearch、alphaevolve、agent-laboratory、rsiagent（research agent 或软件环境，不是机器人 RL）。

## [2026-10-16] approve lens | jev
human 批准。keep：jevany、openjev。
reject：sgs、alphanist、batch-invariant-vlas、sciencediscovery、ctrl-world、roboquest、gemini-4-argon、embodiedevo、embodiedrsi、aspire、rax、rsigym、autoresearch、alphaevolve、agent-laboratory、rsiagent（都不提供返回校准概率的 System 1 决策模型或服务）。

## [2026-10-17] query | Q1
lenses/agent-loop，及 embodiedevo、embodiedrsi、aspire、rax、alphaevolve、agent-laboratory、jevany、rsigym、rsiagent、autoresearch、alphanist 来源页。

## [2026-10-17] query | Q2
sources/gemini-4-argon、lenses/agentic-robotics、log。

## [2026-10-17] query | Q3
lenses/agent-loop，及 alphaevolve、autoresearch、rsigym、embodiedevo、rax、aspire、embodiedrsi、rsiagent、gemini-4-argon、agent-laboratory、roboquest 来源页。

## [2026-10-17] query | Q4
全部 18 个来源页的 published 字段；RSIGym 等 unknown 项另查 raw/。

## [2026-10-17] query | Q5
lenses/agent-loop，及 rsigym、autoresearch、rsiagent、agent-laboratory、alphaevolve、embodiedrsi 来源页。

## [2026-10-18] rename | lenses
robotrsi → agentic-robotics，system1-decision → jev，demo-free-rl → robotics-rl（human）。
