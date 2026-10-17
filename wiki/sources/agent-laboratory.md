---
type: source
url: https://arxiv.org/abs/2501.04227
published: 2025-01
ingested: 2026-10-16
concepts: [人定义评估与验收, 选出集合与确认集合分离, LLM 自评偏高, 人工检查点]
lenses: ["[[agent-loop]]"]
---
# Agent Laboratory

人给研究想法，PhD / Postdoc / ML Engineer 等 LLM agent 走文献综述、实验（mle-solver）、写报告（paper-solver）三阶段，产出代码仓库与报告；人评下论文仍低于 NeurIPS 录用线，LLM 自动评审明显高估。

- **关键数字**：
  - 自主模式：5 题 × 3 后端 = 15 篇，10 名 PhD 志愿者每人评 3 篇。实验质量（1–5）gpt-4o 2.6、o1-mini 3.2、o1-preview 2.9；有用性 4.0 / 4.3 / 4.4。
  - NeurIPS 式人评总分 3.5 / 3.8 / 4.0（满分 10）；NeurIPS 2024 录用均分 5.85。
  - 自动评审 vs 人评：总分 6.1 vs 3.8，clarity 3.6 vs 2.4（满分 4）。
  - Co-pilot 模式（o1-mini）：外部评审总分 4.38，比自主模式高 0.58；研究者打的实验质量 2.38、有用性 3.75，均低于 o1-mini 自主模式。
  - 成本：gpt-4o \$2.33 / 篇、o1-mini \$7.51、o1-preview \$13.10；摘要称比既有自主研究方法降 84%。
  - mle-solver 在 10 个 MLE-Bench 低复杂度文本 / 表格题：4 枚奖牌（2 金 1 银 1 铜），6/10 超人类中位；OpenHands 2 枚、AIDE 2 枚、MLAB 0 枚。
- **评估与接纳**：
  - 流程内接纳由 LLM 定：mle-solver 用 LLM reward model 按研究计划给程序打 0–1 分，高分进 top 程序池；paper-solver 用改编自 The AI Scientist 的 NeurIPS 式 LLM 评审打分，PhD agent 依 3 个评审 agent 的分数决定定稿或回退到早先子任务。
  - 最终质量由人评：PhD 志愿者、co-pilot 研究者自评、外部研究者。作者据自动评审高估约 2.3 分，主张人评须与自动评审并列。
  - MLE-Bench：不用 LLM 打分，在训练集随机切出的 20% dev 集上选程序，最高分代码再上 Kaggle 真实测试集确认。
  - 人工介入：co-pilot 模式在每个子任务末设检查点，人决定继续或带意见重做；研究者反馈难以引导 agent 按自己的确切构想执行，这是 co-pilot 评分下降的原因。
  - LLM 自评与人类评审的一致率低于人与人（53.3% vs 56.1%，引自 The AI Scientist）。
  - 失败模式：文献综述反复调用 summarize 直到步数耗尽（该阶段成功率 60–80%）；实验全 0% 准确率未被纠正；mle-solver 生成 `exit()` 终止进程，需人工检测删除；gpt-4o 报告虚构未发生的实验细节。
- **可信度**：作者自报；人评样本小（15 篇、10 名评审）；MLE-Bench 对比剔除他方无效提交后取均值，mle-solver 跑几次未说明；框架开源。
- **原文**：[[raw/agent-laboratory]]
