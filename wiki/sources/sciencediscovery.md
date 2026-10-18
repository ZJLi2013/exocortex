---
type: source
url: https://github.com/openJiuwen-ai/sciencediscovery
published: unknown
ingested: 2026-10-16
tags: []
concepts: [结果溯源, 沙箱代码执行, 执行前人工授权, 多 agent 编排]
benchmarks: []
methods: []
models_used: []
models_compared: []
lenses: ["[[agent-loop]]"]
---
# ScienceDiscovery

本地运行的科研工作台：agent 读文献、在沙箱里写并运行代码，并为每个结果记录来源；README 不给任何性能结果。

- **关键数字**：
  - 无效果或基准数字。
  - 版本 Release 0.2.0；Linux x86_64 / aarch64 预编译二进制，macOS 走源码模式。
  - 不内置模型，用户自接 API key；基于 JiuwenSwarm。
- **评估与接纳**：README 未给评估协议，谁宣布成功、在哪个集合上选出或确认均未说明。
  首次代码执行前弹出权限卡，由人批准后才执行；每个交付物记录代码、环境、日志与引用证据，供事后审查。
  agent 在 fail-closed 沙箱内运行 Python、R、shell；agent 不能改的范围除此之外未说明。
- **可信度**：产品 README，无实验或评测；Apache 2.0 开源。
- **原文**：[[raw/sciencediscovery]]
