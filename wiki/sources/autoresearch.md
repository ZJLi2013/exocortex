---
type: source
url: https://github.com/karpathy/autoresearch
published: 2026-03
ingested: 2026-10-16
tags: []
concepts: [人定义评估与验收, 贪心接受, 固定时长预算]
benchmarks: []
methods: []
models_used: []
models_compared: []
lenses: ["[[agent-loop]]"]
---
# autoresearch

AI agent 通宵改单 GPU 的小型 LLM 训练代码，每次训 5 分钟、看 val_bpb 是否变好、保留或丢弃，循环往复；README 不报具体提升幅度。

- **关键数字**：
  - 每次实验固定 5 分钟墙钟训练（不含启动 / 编译），约 12 次 / 小时、一夜约 100 次。
  - 指标 val_bpb（越低越好，与词表大小无关）；单张 NVIDIA GPU，在 H100 上测试。
  - 无最终 val_bpb 或提升幅度数字。
- **评估与接纳**：评估由人写死在 `prepare.py`（常量、数据准备、dataloader、evaluation），标明不可修改。
  agent 只改 `train.py`（架构、超参、优化器、batch size 均可改）；人改 `program.md` 指令。
  接纳规则：val_bpb 变好就保留，否则丢弃；选出与确认用的是同一个验证指标，独立确认集合或多 seed 未说明。
  固定时长让同一平台内结果可比，跨平台不可比。
- **可信度**：作者 README，无报告结果；MIT 开源；`program.md` 刻意保持为最简基线。
