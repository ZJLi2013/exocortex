---
type: source
url: https://github.com/QwenLM/BlenderWorld
published: 2026-10-14
ingested: 2026-10-24
tags: []
concepts: [真实参考驱动的 3D 创作评测, 多视角渲染与场景检查, 二元 rubric 与视觉质量融合, 生成与评测容器隔离]
benchmarks: []
methods: []
models_used: ["[[GPT-6 Astra]]", "[[Claude Opus 5]]", "[[GPT-5.6 Sol]]", "[[deepseek-v4-1-flash]]", "[[Qwen3.8-Max]]", "[[glm-5-3-flash]]", "[[Grok-4.6]]", "[[Claude Opus 4.8]]", "[[Seed2.1-Pro-0915]]", "[[Qwen3.8-27B]]", "[[Kimi-K3]]", "[[Gemini 3.8 Flash]]", "[[MiniMax-M3]]", "[[GPT-5.6 Terra]]"]
models_compared: ["[[Claude Opus 5]]", "[[GPT-5.6 Sol]]", "[[deepseek-v4-1-flash]]", "[[Qwen3.8-Max]]", "[[glm-5-3-flash]]", "[[Grok-4.6]]", "[[Claude Opus 4.8]]", "[[Seed2.1-Pro-0915]]", "[[Qwen3.8-27B]]", "[[Kimi-K3]]", "[[Gemini 3.8 Flash]]", "[[MiniMax-M3]]"]
lenses: ["[[agentic-3d]]"]
---
# BlenderWorld

让视觉 agent 按真实世界的文字、图片或视频参考，在 Blender 里交付可编辑工程；223 个任务、2,651 条二元 rubric，13 个前沿模型里 GPT-6 Astra 融合分最高 79.9。

- **关键数字**（每个任务只跑一次，各模型最高 reasoning 档）：
  - 总融合分：GPT-6 Astra 79.9（文本 78.6 / 多模态 80.7，Rubric 87.3 / Dimension 72.6，全 rubric 通过率 42.2%）；Claude Opus 5 73.0；GPT-5.6 Sol 67.7；DeepSeek-V4.1-Flash 65.7；Qwen3.8-Max 60.6；GLM-5.3-Flash 59.7；Grok-4.6 与 Claude Opus 4.8 各 57.0；Seed2.1-Pro-0915 51.3；Qwen3.8-27B 47.7；Kimi-K3 46.5；Gemini 3.8 Flash 34.2；MiniMax-M3 31.8。
  - 第二名的全 rubric 通过率：Claude Opus 5 25.6%，其余不超过 15.7%。
  - 规模：223 题 = 78 文本 + 130 图 + 文 + 15 视频 + 文；9 个类别、16 个应用场景，59 题附尺寸 / 材质 / 相机规格文件。
- **评估与接纳**：生成与评测在不同容器，rubric 对 agent 不可见；评测渲染 8 个自适应视角（Cycles、1024×1024、64 samples，每视角最多补渲两次），二元 rubric 按权重 1/2/3 计分，另由 VLM 给 8 个视觉质量维度 1–10 分，两者各占 50%。没有 `.blend` 提交直接 0 分。GPT-5.6 Terra 同时当渲染、rubric 与维度裁判；作者用 147 对人工偏好验证裁判，它的总体一致率 82.99%，Gemini 3.8 Flash 77.55%、DeepSeek-V4.1-Flash 76.87%，分差小的子集降到 68.57 / 58.57 / 55.71%。
- **可信度**：作者自报，每题单次尝试；生成 rubric 时用 GPT-5.6 Sol 起草、至少两个独立模型复核；数据集公开，代码 MIT。
- **模型**：GPT-6 Astra 与 GPT-5.6 Sol 用 Codex，其余 11 个 agent 用 Claude Code；GPT-5.6 Terra 是裁判。
