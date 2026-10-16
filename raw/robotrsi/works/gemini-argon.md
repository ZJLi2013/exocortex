# 基座模型接过整条链路：Gemini 4 Argon

**Gemini 4 Argon 把一个通用多模态基座用在机器人链路的每一段：控制、Real2Sim、判分、造数据、硬件上自改进。它直接出动作时仍经固定原语；全文唯一的任务级增益落在 VLA 权重上。**
[博客](https://developers.googleblog.com/gemini-4-argon-for-robotics/)（2026-10-13）给的是 prompt 与演示；ERQA 87% 是纯推理题的分数，不是任务成功率。

| 用法 | Argon 的角色 | 在本页的位置 |
|---|---|---|
| 零样本控制、Spot 踩踏板扔罐子 | 调固定原语（`grasp`、`place_until_contact`、`move_by`），配视觉坐标网格；放手前由验证 agent 确认 | L3，与 RoboRSI 的 Engineer 同一形态 |
| Omni 控制 | 给视频世界模型写带时间戳的动作 prompt，看关键帧后改写 | 模型当世界模型的控制器 |
| Real2Sim（机器人视频、人类第一视角视频、手绘草图） | 重建 MuJoCo 孪生，按视觉一致与指尖接触力一致两个目标迭代 | agent 造环境 |
| 事后标注、价值函数 | 四级时间对齐标注；密集进度曲线；重试段进度持平并降权 | 判分器 / critic，与 TOPReward、Jev 同位 |
| 仿真造数据 | 一张照片 → 孪生 → 77 个任务 → 4,500+ 条 `reward == 1.0` 轨迹 → 微调 VLA | 写回落到权重 |
| SO-101 硬件自改进 | 失败后自己读日志与录像、dry run 验证修复、重试，成功后提速 | episode 间改程序；三个阶段与安全规则（`AGENTS.md`）由人写 |

- **直接控制没有成功率。** 零样本控制按调用粒度分三档，最细一档是 8–20 次调用的视觉伺服；接触靠 `move_until_contact` 这类力控原语。RoboProbe「语义强、精密接触弱」的结论在这里没有被检验。
- **增益读数都是单次。** 56% → 75% 没给评测次数；SO-101 报的是三轮各一次的耗时：58.9 s、22.9 s（擦到盒沿）、17.4 s。
- **闭源付费。** `gemini-4-argon` 走 Gemini API 付费档与 AI Studio，模型版本不能冻结在某个 release 上。

对本页判断的影响：

- 开头的判断成立且往外延伸：基座不只坐在快环里，还接过建仿真、定义任务、判分这些原本由人做的环节，因此介入方式补成四类。
- 复杂 harness 的分工会被单模型吸收：硬件自改进是一个 prompt 分三段，人只写阶段、安全规则与验收。留下来的是环境原生 verifier 与冻结评测口径、原语接口（尤其 VLA 支撑的接触原语）、回流到权重的数据管线，对应[改进方向](../direction.md#改进方向) 1、2、4。
- 判分与价值函数对应 [frozen VLM reward](../../../rlinf/doc/features/frozen_vlm_rewards/rl_reward.md)，驱动视频世界模型对应 [wm_forge](../../../wm_forge/readme.md)。两处都可以把 Argon 当上界参照，前提是接受付费 API 依赖。

## 可信度

Gemini 4 Argon 的描述与读数只来自 Google Developers Blog（2026-10-13）的 prompt 与演示视频说明；没有论文或技术报告，评测次数、成本与延迟均未公开。
