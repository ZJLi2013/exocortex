---
type: lens
tags: [llm-foundation-models]
---
# llm-foundation-models

## 范围

会改变「agent 选哪个基座、按什么上下文成本来用」的基础模型发布。

## 问题

### Q1 agent 选哪个基座？
当前答案：未定：各家 agent 基准都是自报，harness 不同或未说明，不能横比。依据 C3

### Q2 按什么上下文成本来用？
当前答案：Flash 档用 8–18B 激活与压缩的 KV cache 降低长上下文成本，可作长上下文默认档；「接近旗舰」都是自报。依据 C1、C2

## 判断

### C1 Flash 档基座用架构压缩 KV cache 与注意力计算
- 回答：Q2
- 支持：
  - [[deepseek-v4-1-flash]]（自报）KV cache 相对上一代只需 1/4 HBM、1/8 SSD
  - [[glm-5-3-flash]]（自报）相对 GLM-5.3，每层 KV cache 小 4.4×，每头每层注意力计算少 3.0×
- 限定：
  - [[deepseek-v4-1-flash]]（自报）对比的上一代未点名
- 反驳：—
- 推翻：独立实测的 KV cache 占用没有按自报比例下降

### C2 激活参数降到 8–18B，agent 基准仍接近或超过上一代旗舰
- 回答：Q2
- 支持：
  - [[glm-5-3-flash]]（自报）18B 激活，DeepSWE v1.1 63.4，GLM-5.2 为 46.2
- 限定：
  - [[deepseek-v4-1-flash]]（自报）输入 8B、输出 16B 激活，称超过 V4-Pro，但未给基准名与分数
- 反驳：—
- 推翻：同一 harness 的独立评测下，与旗舰差距显著

### C3 同为 DeepSWE v1.1，各家用的 harness 不同或未说明
- 回答：Q1
- 支持：
  - [[deepseek-v4-1-flash-1017]]（自报）77.0，Mini-SWE-V2
  - [[muse-spark]]（自报）75.4，harness 未说明
  - [[mimo-v2-6]]（自报）Pro 72.57，harness 未说明
  - [[glm-5-3-flash]]（自报）63.4，mini-swe-agent
- 限定：—
- 反驳：—
- 推翻：同一 harness 下由第三方统一重跑

## 冲突
