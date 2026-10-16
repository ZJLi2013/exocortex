# log

## [2026-10-16] ingest | RSIGym
agent-loop keep；robotrsi reject（不涉及机器人）。

## [2026-10-16] ingest | EmbodiedEvo
robotrsi keep；agent-loop keep。

## [2026-10-16] ingest | Gemini 4 Argon
robotrsi keep；agent-loop reject（硬件自改进的阶段由人写，不是 research agent）。

## [2026-10-16] ingest | ScienceDiscovery
robotrsi reject（不涉及机器人）；agent-loop reject（只有产品功能描述，无评估或结果）。

## [2026-10-16] ingest | autoresearch
agent-loop keep；robotrsi reject（LLM 训练，不涉及机器人）。

## [2026-10-16] ingest | RAX
robotrsi keep；agent-loop keep。

## [2026-10-16] ingest | AlphaEvolve
agent-loop keep；robotrsi reject（不涉及机器人）。

## [2026-10-16] ingest | Agent Laboratory
agent-loop keep；robotrsi reject（不涉及机器人）。

## [2026-10-16] ingest | RSIAgent
agent-loop keep；robotrsi reject（软件环境，不涉及机器人）。

## [2026-10-16] ingest | EmbodiedRSI
robotrsi keep；agent-loop keep。

## [2026-10-16] ingest | RoboQuest
robotrsi keep；agent-loop reject（评测前沿模型当单回合机器人策略，不是 research agent）。

## [2026-10-16] ingest | ASPIRE
robotrsi keep；agent-loop keep。

## [2026-10-16] lint | 新建概念页
经验写成代码技能、跨模型迁移、验证 agent、进化式代码搜索（ASPIRE 的「程序进化搜索」并入）。

## [2026-10-16] query | Q1
concepts/选出集合与确认集合分离、lenses/agent-loop，及 embodiedevo、embodiedrsi、aspire、rax、alphaevolve、agent-laboratory、rsigym、rsiagent、autoresearch 来源页。

## [2026-10-16] query | Q2
sources/gemini-4-argon、concepts/验证 agent、lenses/robotrsi、log。

## [2026-10-16] query | Q3
concepts/人定义评估与验收、lenses/agent-loop，及该概念页列出的 11 个来源页。

## [2026-10-16] query | Q4
全部 12 个来源页的 published 字段；RSIGym、RAX 另查 raw/rsigym、raw/rax。

## [2026-10-16] query | Q5
concepts/自改进、concepts/选出集合与确认集合分离、lenses/agent-loop，及 rsigym、rsiagent、autoresearch、alphaevolve、embodiedrsi 来源页。

## [2026-10-16] ingest | JevAny
robotrsi reject（机器人只在 playground 回放，无机器人结果）；agent-loop reject（决策模型基础设施，不是 research agent 或自改进系统）。

## [2026-10-16] ingest | OpenJev
robotrsi reject（不涉及机器人）；agent-loop reject（决策推理服务器，不是 research agent 或自改进系统）。

## [2026-10-16] ingest | SGS
robotrsi reject（纯 RL 训练课程，无 agent）；agent-loop reject（不是 research agent 或自改进系统）。

## [2026-10-16] ingest | AlphaNIST
robotrsi reject（纯 RL 训练，无 agent，只有训练成功率）；agent-loop reject（不是 research agent 或自改进系统）。

## [2026-10-16] ingest | Ctrl-World
robotrsi keep；agent-loop reject（README 只有世界模型推理与训练，无 agent 循环）。

## [2026-10-16] ingest | Batch-Invariant VLAs
robotrsi reject（VLA 推理数值工程，无 agent，不改选底座、改进方向或评测选择）；agent-loop reject（不涉及 research agent）。
