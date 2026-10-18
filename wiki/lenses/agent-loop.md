---
type: lens
tags: [agent-loop]
---
# agent-loop

## 范围

agent 自主提出改动、跑实验、按评估决定接纳的研究或自改进循环，限于不绑定领域的框架或在非机器人任务上验证的工作。

## 总结

包括在固定评估下搜代码的系统、自主走完研究流程的 agent、评测这类 agent 的环境，以及一个科研工作台。接纳依据有程序化评估器，也有 LLM 判定。全部是自报。

## 工作

- [[agent-laboratory]]：LLM agent 走文献综述、实验、写报告三阶段；人评 3.5–4.0 / 10，LLM 自动评审给 6.1、人评 3.8。（自报）
- [[alphaevolve]]：LLM 对代码提 diff，按用户写的评估函数进化迭代；找到 4×4 复矩阵 48 次乘法，Borg 调度回收 0.7% 算力。（自报）
- [[autoresearch]]：agent 改单 GPU LLM 训练代码，每次训 5 分钟，val_bpb 变好就保留；不报提升幅度。（自报）
- [[rsiagent]]：curriculum / actor / verifier 三个 agent 自主练习，经验写进 memory；OSWorld 2.0 71.97 → 78.98。（自报）
- [[rsigym]]：研究 agent 改另一个系统的数据或 harness 的环境；30 个 Joint run 有 29 个超过初始系统。（自报）
- [[harness2]]：权重不变，在同一任务上提改动、试跑、按执行对比合成新 harness，经验带到后续任务；单步 WorkBuddy-Bench 最多 +11.5 分。（自报）
- [[sciencediscovery]]：本地科研工作台，沙箱跑代码并为每个结果记录来源；不报性能。（自报）

## 冲突
