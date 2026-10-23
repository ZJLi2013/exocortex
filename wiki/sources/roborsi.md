---
type: source
url: https://github.com/nssmd/RoboRSI
published: 2026-10-08
ingested: 2026-10-24
tags: []
concepts: [自改进, 失败归因, 层级技能树限定修改范围, 后置条件验证]
benchmarks: ["[[LIBERO]]", "[[LIBERO-Pro]]", "[[LIBERO-Plus]]", "[[RoboTwin]]"]
methods: ["[[harness evolution]]", "[[code skills from experience]]"]
models_used: ["[[GPT-5.6 Sol]]", "[[ACT]]"]
models_compared: []
lenses: ["[[agentic-robotics]]"]
---
# RoboRSI

Manager / Planner / Engineer / Reviewer 四个 agent 按任务–技能树执行与改技能：失败归到最早出问题的节点、只改那一支，后置条件通过后才发布；真机 104 轮学家庭清理，四个仿真基准成功率都最高。

- **关键数字**（全部用 GPT-5.6 Sol，同一工具接口与每回合预算）：
  - LIBERO：84/150（56.0%），对照 OpenETA 76/150（50.7%）；覆盖 24/30。
  - LIBERO-PRO：297/600（49.5%），对照 OpenETA 231/600（38.5%）；覆盖 102/120；Object 套件 +16.5 点、物体扰动 +15.3 点。
  - LIBERO-Plus（冻结 LIBERO 库）：354/840（42.1%），对照 OpenETA 306/840（36.4%）；覆盖 28/30。
  - RoboTwin：37/154（24.0%），对照 OpenETA 32/150（21.3%）；覆盖 26/50。
  - 真机 WheelSingleArm M1：104 轮、24 小时累计运行；早期一轮放置 0 个物体，后期有整轮完成并回坞；两场景演示分别放好 5 / 4 个目标物，换场景不改技能与配置、无人工纠正。
  - 消融：RoboTwin 上分工 36/50 对单 Engineer 9/50；600 对匹配 episode 里复合技能把成功率从 21.5% 提到 29.0%（+7.5 点，95% CI 3.7–11.5，McNemar p<10⁻⁴），token / 模型调用 / 墙钟中位数降 29.4% / 27.2% / 17.0%；同一失败上 TSR 改 3 个文件 50 行、2/2 种子通过并发布，平铺修改两个候选都只过 1/2、未发布。
- **评估与接纳**：自改进算被评能力——LIBERO、LIBERO-PRO、RoboTwin 上边评边改，LIBERO-Plus 用冻结库测迁移；基线是同一骨干、工具与预算的固定技能系统。成功只由仿真器谓词在 agent 循环结束后判定，journal 只追加，`roborsi eval-audit` 独立重算分数。
- **可信度**：作者自报；真机放置由现场人员确认，选中运行不能隔离单次修改的效果；在线自改进结果随模型与运行变化，README 称不保证与表格完全一致；代码开源。
- **模型**：GPT-5.6 Sol 是所有方法共用的骨干；ACT 用执行数据训练成工具，10,000 步，相对关节目标在训练布局上 click_bell 4/10、click_alarmclock 6/7、未见布局 2/3，绝对目标全部失败。Manager 等四个是角色，不是模型。
