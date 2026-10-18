---
type: source
url: https://cyberneticphysics.com/blog/batch-invariant-vlas
published: 2026-09-04
ingested: 2026-10-16
tags: []
concepts: [批不变推理, 推理非确定性, 逐层张量追踪定位发散]
benchmarks: []
methods: []
models_used: ["[[π0]]"]
models_compared: []
lenses: []
---
# Batch-Invariant VLAs

Cybernetic Physics 把 π0 推理做成批不变：同一输入在 batch = 1 与 batch = 32 下最终动作逐元素一致；只开 Thinking Machines 的批不变算子不够，还要换掉 SigLIP 的 Conv2d patch 投影，并把 rank-4 matmul 拆成二维 `torch.mm`。

- **关键数字**：
  - 单测 SigLIP patch 投影 Conv2d（3 → 1152，14×14 核与步长）：batch 1–16 max abs diff 0，batch 32 为 0.000903。
  - 只开批不变算子：从 SigLIP patch embedding 起全部张量发散。修 patch 投影后，第一处发散移到 joint model 注意力的 `torch.matmul`：rank-4 输入走 `aten::bmm`，绕过了批不变的 `aten::mm`。
  - 全部修完后 batch 32（1 个参考 + 31 个干扰样本，1 次试验）：max / mean abs diff、RMSE、relative L2 全为 0.0；参考 1.27 s，batch 平均 23.62 s，吞吐为参考的 1.72×。
- **评估与接纳**：
  - 判据是 batch 1 参考与 batch 32 第 0 个样本的逐张量差，由作者自写的 tracer 记录。
  - 只跑 1 次试验；未在机器人上测对行为的影响。
- **可信度**：公司博客，作者自报，单次；2026-09-22 修订；称代码在 GitHub；当前实现逐个矩阵乘、慢。
- **模型**：研究对象是 π0 的推理路径。
- **原文**：[[raw/batch-invariant-vlas]]
