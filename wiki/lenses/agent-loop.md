---
type: lens
---
# agent-loop

## 范围

会改变 agent-loop 探索模式、评估 / 预算 / 人工介入设计的 research agent 与自改进系统。

## 当前判断

1. 能稳定涨分的 research agent 都跑在它改不了的评估协议、按服务计费的预算和事后审计之内。
2. 在小开发集上自己挑候选的自改进没有迁移到全集。
3. 探索模式里，确认胜出分支所用的集合不能是选出它的那个集合。
4. 自改 harness 只在有固定 benchmark 时被证明有效；本库没有这类 benchmark，维持不做自改进。
5. 信号先于搜索：没有程序化评估器就不做进化搜索（AlphaEvolve 是主要依据）。
6. 贪心接受规则是反例（autoresearch）；否定记录要活过回滚。
7. human 随时介入比只在时间盒末介入好；「难以引导」是后者的反例依据（Agent Laboratory）。
8. 不用 LLM 打分当实时信号。

## 待批准

> [!draft] RSIGym（2026-10-16）
> 支持判断 1、2、4：评估协议、服务预算与事后审计都由任务定义锁定；Qwen3.8 在 6 题开发集上的增益没迁移到 37 题全集；Harness track 的涨分建立在固定 Terminal-Bench 上。依据 [[rsigym]]

> [!draft] EmbodiedEvo（2026-10-16）
> 支持判断 3：Playground 与 Test 用不同布局，经验冻结后才评测，Test 只读不能 reset。依据 [[embodiedevo]]

> [!draft] AlphaEvolve（2026-10-16）
> 支持判断 5：只适用于能写出自动评估器的问题；Borg 与 kernel 的选出 / 确认分开，矩阵乘与数学问题没有独立确认集。依据 [[alphaevolve]]

> [!draft] autoresearch（2026-10-16）
> 支持判断 1、6：评估写死在人写的 `prepare.py`、每次固定 5 分钟；val_bpb 变好即保留，选出与确认同一指标，是贪心接受的反例来源。依据 [[autoresearch]]

> [!draft] Agent Laboratory（2026-10-16）
> 支持判断 7、8：co-pilot 只在子任务末设检查点，研究者反馈难以引导，评分低于自主模式；LLM 自动评审比人评高约 2.3 分。依据 [[agent-laboratory]]

> [!draft] RSIAgent（2026-10-16）
> 支持判断 3（反例）：练习与最终评测是同一目标任务；verifier 在官方 rubric 下仍误判 PASS，未验证的决定被写成规则复用。依据 [[rsiagent]]

> [!draft] RAX（2026-10-16）
> 支持判断 3：正式评测用从未见过的 held-out 布局，recorder 对 agent 只读；探索布局与 seed 数未说明。依据 [[rax]]

> [!draft] EmbodiedRSI（2026-10-16）
> 支持判断 3，并给探索模式一种新做法：按「信息增益 / 实验成本」选下一个实验，50 个 episode 时 72.9% vs 随机 27.1%。依据 [[embodiedrsi]]

> [!draft] ASPIRE（2026-10-16）
> 支持判断 3、5：进化搜索跑在固定协议与程序化仿真成功信号之上，选出 / 确认 seed 分离；循环很耗算力。依据 [[aspire]]
