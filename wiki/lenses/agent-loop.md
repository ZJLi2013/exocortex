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
