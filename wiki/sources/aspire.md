---
type: source
url: https://research.nvidia.com/labs/gear/aspire/
published: 2026-07
ingested: 2026-10-16
tags: []
concepts: [选出集合与确认集合分离, 人定义评估与验收, harness 演化, 自改进, 经验写成代码技能, 跨模型迁移, 进化式代码搜索]
benchmarks: ["[[LIBERO-Pro]]", "[[Robosuite]]", "[[BEHAVIOR-1K]]"]
lenses: ["[[agentic-robotics]]"]
---
# ASPIRE

coding agent 从执行 trace 诊断失败、修 code-as-policy 程序，把验证过的修复存进技能库，并用进化搜索探索多条程序；Opus 5.5 下 LIBERO-Pro 平均 99%。

- **关键数字**：
  - 相对已有方法：扰动操作任务最多高 77%，Robosuite 双臂交接高 72%，长程家务最多高 32%。
  - 技能库零样本用到未见长程任务：31% vs 已有方法 4%。
  - Claude Opus 5.5：LIBERO-Pro 全部 80 个任务平均 99%；代表性 Robosuite 与 BEHAVIOR-1K 任务 100%。
  - 真机：带仿真里发现的技能时，首次真机成功所需 token 更少、held-out 成功率更高（具体数值只在图表里）；跨具身示例中仿真用 Claude Opus 4.6、真机用 GPT-5.5。
  - GPT-6 Astra 在真机上在线学魔方，每转一面的 token 与耗时随 episode 下降。
- **评估与接纳**：
  - 在小的 debug split 上学习，在互不相交的 held-out seed 上报告成功率：LIBERO-Pro 每任务 50 个、Robosuite 100 个、BEHAVIOR-1K 25 个。
  - 基线 CaP-Agent0 每个 seed 重新生成程序，可用测试时推理与重试。
  - 换模型对比时环境、机器人编程 API、评估协议固定。成功由谁判定未说明。
  - agent 只能调用预定义的感知 / 规划 / 控制原语 API，原语集合固定。
  - 真机还不能自主学习：成功检测、安全 reset、安全监控与标定仍需解决。
- **可信度**：项目页，作者自报；评测次数与方差未说明；LIBERO-Pro 任务数页内写法不一（摘要 80 个，结果节 160 个）；依赖冻结的前沿 LLM，搜索循环耗费大量 LLM 调用和 rollout；代码链接 NVlabs/ASPIRE。页面未写发布日期，BibTeX 引 arXiv:2607.00272。
- **原文**：[[raw/aspire]]
