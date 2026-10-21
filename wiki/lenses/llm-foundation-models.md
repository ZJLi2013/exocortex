---
type: lens
tags: [llm-foundation-models]
---
# llm-foundation-models

## 范围

agent 可用的前沿基础模型发布。

## 总结

5 个通用 agent / 编码模型、1 个物理推理基座。各家基准版本与 harness 不一，数字跨来源不可直接比。全部是自报。

## 工作

- [[glm-5-3-flash]]：智谱首个原生多模态 GLM-5 模型，320B 总参、18B 激活，线性加稀疏注意力；DeepSWE v1.1 63.4。（自报）
- [[muse-spark]]：Meta 面向长程 agent 与编码的模型，1M 上下文；DeepSWE v1.1 75.4、Terminal-Bench 2.1 88.8。（自报）
- [[deepseek-v4-1-flash]]：552B MoE、原生视觉，KV cache 为上一代 1/4；未公布基准数字。（自报）
- [[mimo-v2-6]]：小米开源全模态系列，加大可验证任务上的 RL 算力；held-out DeepSWE v1.1 Pro 58.4 → 72.57。（自报）
- [[gemini-4-argon]]：Google 物理推理基座；仿真造数据后真机成功率 56% → 75%，未给评测次数。（自报，博客）
- [[deepseek-v4-1-flash-1017]]：V4.1-Flash 小版本更新，输出更短；Terminal-Bench 4.0 31.2 → 42.3。（自报）
