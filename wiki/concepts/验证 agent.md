---
type: concept
---
# 验证 agent

由独立于执行者的 agent 判定结果是否通过，执行者不能自己宣布成功。

## 来源
- [[gemini-4-argon]]：Spot 演示用 foot / hand 两个验证 agent 确认后才释放。
- [[rsiagent]]：verifier（独立上下文，看不到 actor 推理与 memory）判 PASS / FAIL；在官方 rubric 下仍会误判 PASS。
