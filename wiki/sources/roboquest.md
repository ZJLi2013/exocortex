---
type: source
url: https://arxiv.org/abs/2610.10388
published: 2026-10
ingested: 2026-10-16
tags: []
concepts: [人定义评估与验收, 主动探索取证, 自主判断何时提交, 失败归因]
lenses: ["[[agentic-robotics]]"]
---
# RoboQuest

10 个需要靠物理交互取证（搜索、检查、测试）的移动操作 benchmark；最好的前沿模型 GPT-6 Astra 只成功 23.2%，失败主要来自探索不足和过早决策，执行只占少数。

- **关键数字**：
  - 成功率（每格 50 episode）：GPT-6 Astra 23.2%、Opus 5.5 13.8%、GPT-6.1 Sol 12.2%、Fable 5.1 11.4%、Gemini 3.8 Flash 2.0%；去掉最容易的 Puzzle Box 后最高 15.1%。
  - 5,000 条示范 SFT 的 π0.5：Puzzle Box 2.0%，其余任务 0%。
  - 执行技能单测（给出隐藏信息，每技能 20 个场景）：72–81%。
  - 失败归因（Astra / Opus 5.5 / Sol）：缺证据 43 / 43 / 46%，错误决策 23 / 31 / 25%，执行 21 / 19 / 18%，副作用 13 / 7 / 12%。
  - Puzzle Box 遮住锁链：Opus 5.5 94.4% → 36.8%，Astra 不受影响。
  - 五个模型评测总花费 \$21,352。
- **评估与接纳**：
  - 机器人按下场景里的 SUBMIT 按钮才结束并冻结分数；何时提交由 agent 自己判断，不按算失败。成功 = 按下时每个目标条件都成立，由 benchmark 的规则判定。
  - 隐藏信息存在 agent 读不到的私有 specification 里；所有模型跑同一批 50 个实例 / 任务。
  - 示范与评测集不共享实例；评测集另外 hold out 厨房风格和部分任务配置。
  - agent 只有 ARM / BASE / WAIT / STOP 四个工具，没有定位或抓取工具；上限 200 次决策，图像只留最近两帧。
  - 失败归因用每个任务的有序确定性规则逐个未满足条件打标签，规则与标签随 benchmark 发布。
- **可信度**：作者自报；每个模型在每个实例上跑一次；归因规则、标签与示范数据集（LeRobot v2.1）随 benchmark 发布。
- **原文**：[[raw/roboquest]]
