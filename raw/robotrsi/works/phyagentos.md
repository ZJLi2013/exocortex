# LLM 编排冻结 VLA 的开源框架：PhyAgentOS

**PhyAgentOS 把「认知规划 → 物理执行 → 任务验证」连成一个环，从验证过的经验里积累 Skills 与 Lessons。它是 L2 形态（LLM + π0.5）目前最成熟的开源框架；
公开数字里 π0.5 的加入让 GPT-6 在 RoboDojo 上从 8.3% 到 23.3%，但抽样口径太松，不能当方法对比。**
分级 L2（也支持纯 LLM 与纯动作模型两种模式），写回是带版本的 Skills 与 scoped Lessons。[代码](https://github.com/PhyAgentOS/PhyAgentOS-core)（MIT，v1.1.0 于 2026-10-09），技术报告 arXiv:2607.16636（中山大学 HCP Lab / 鹏城实验室 / X-Era Lab）。

- **物理执行是一个可安装的 Skill 包**：bundle 声明工作流文档、所需工具 ID、命名的运行时 profile 与按平台锁定 SHA-256 的执行节点，由 Dora 管理运行时。Core 不带模型权重、仿真资产或机器人驱动。
- **验证与进化有配置上限**：每 episode 最多重规划 2 次；进化默认 `guarded_auto`，至少 3 个成功 episode 才晋升 workflow、3 个 episode 才写 Lesson，每个 Skill 最多 8 条 Lesson。
- **v1.1.0 的 governed interaction**（可选）：AgentTask 与 Session 经冻结绑定、持久 Runner 与 Supervisor 接到多步决策和独立的根验证。

| 配置 | LIBERO-10 | RoboDojo | RoboTwin |
|---|---|---|---|
| GPT-6 + π0.5 | 100.00% | 23.30% | 76.70% |
| DeepSeek 4.1 Flash + π0.5 | 97.22% | 26.70% | 77.80% |
| Gemini Robotic ER2 + π0.5 | — | — | 80.00% |
| DeepSeek 4.1 Flash | 82.00% | 8.30% | — |
| GPT-6 | — | 8.30% | — |

对 RobotRSI 判断的影响：

- 形态与 [vla-executor](../../roborsi/exps/vla_executor/readme.md) 要做的事一致：LLM 规划，冻结 π0.5 当执行 Skill。它与 RPent 都可以当 L2 对照；PhyAgentOS 的 LIBERO profile 走 MuJoCo，理论上能在 MI300 上跑，未验证。
- 接纳门是「成功次数够了就晋升」，不配对、不留出 seed、不做历史回归，比 EmbodiedRSI 与 EmbodiedEvo 的协议弱，属于本页「接纳权限」轴上的弱门禁。
- LIBERO-10 已到 100%，这个场地区分不了方法；RoboDojo 上的 π0.5 增益与 GPT-as-Policy（26% → 48%）方向一致。

## 可信度

- 数字只来自仓库 README（核于 2026-10-16），未读技术报告。RoboDojo 与 RoboTwin 各只随机抽 10 个任务，部分模型的样本数不同；排行榜参照可能用了不同协议。
- 进化是否让同一任务的成功率逐轮上升，README 没有给出数字。
