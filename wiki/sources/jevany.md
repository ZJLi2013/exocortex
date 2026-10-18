---
type: source
url: https://github.com/SimpleJev/JevAny
published: unknown
ingested: 2026-10-16
concepts: [System 1 决策模型, 选项概率读出, 概率校准, LLM 规划加小模型选动作]
lenses: ["[[system1-decision]]"]
---
# JevAny

System 1 决策模型的开源训练与部署框架：输入状态、问题与候选项，直接返回选择及其概率；默认发布的 JevAny-Qwen3.8-27B 在 Transfer 86.04%、JevBench 90.04%，两项均为其发布表最高。

- **关键数字**：
  - JevAny-Qwen3.8-27B（LoRA，pointer 读出）：Transfer 86.04%、JevBench 90.04%；Transfer 上 NLL 0.388、Brier 0.195、ECE 0.026。基线 Jev 1.13.0 为 85.37% / 86.58%，Kev-27B 为 82.31% / 85.28%。
  - 外部零样本：Typed 72.8%、JevJudge full 62.3%、text 子集 66.4%；Jev 1.13 为 Typed 72.7%、text 65.1%。
  - 免训练 choice-token 读出：冻结 4B 在 Typed 52.75%，Direct-Token 训练后 64.80%；27B blend 在 JevJudge text 上 66.44% → 64.36%（变差）。
  - H200 上 27B 中位延迟 113.54 → 30.53 ms（3.72×），JevBench 公开 231 题准确率前后都是 89.61%。
  - agent loop 演示（各一对录制回放）：WebShop 只用 LLM 9 步 18.54 s，LLM + Jev 5 步 7.83 s；Terminal-Bench `sqlite-db-truncate` 13 条命令 187.9 s → 7 条 144.7 s。
  - 训练数据：1,772,725 条文本记录、2,180,242 个标注决策，SFT 训练 LoRA。
- **评估与接纳**：
  - 作者在 Transfer、JevBench、Typed Decisions、JevJudge 上评测，协议在外部文档。
  - choice-token blend 权重在开发数据上调好后冻结再评测。
  - agent loop 演示每个环境只有一对录制，不是统计评测。
  - 机器人只出现在 playground：Franka 插销由 PyBullet 接触物理判成功，GIF 是旧 checkpoint 的回放，未给机器人成功率。
- **可信度**：作者自报；评测次数与方差未说明；代码与起步数据 Apache-2.0 开源，权重发布在 Hugging Face。
- **原文**：[[raw/jevany]]
