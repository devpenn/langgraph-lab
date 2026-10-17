# Stage 10 · 可观测与评估（2h）

agent 出错时「黑盒里发生了什么」必须能看清；改 prompt 必须有分数说话。

```bash
uv sync --extra obs    # 装 langsmith（也可用 Langfuse 自托管替代，概念相同）
```

## 核心概念

- **LangSmith tracing**：设 `LANGSMITH_TRACING=true` + key 即全量采集——每次 run 的每步输入输出、token、延迟、树状调用结构
- **没有账号的替代**：Langfuse（可自托管），或自己写一个 callback handler 把每步打印到终端（理解原理用）
- **Eval 三件套**：Dataset（输入 + 期望）+ Evaluator（规则或 LLM 打分）+ 实验对比

## 动手项目：给 agent 建分数基线（代码写在 `10/`）

1. 打开 tracing，跑 3 个 Stage 3 的任务，在网页里找到一次工具调用失败的全链路 trace
2. 建 10 条只读命令任务的小数据集，用「是否调对了工具」做 evaluator，跑出基线分
3. 改一次 system prompt（收紧工具白名单的描述），对比前后分数

## 验收清单

- [ ] 能在 trace 里定位一次失败 run 的根因
- [ ] 有一个可重复执行的 eval 脚本，且分数变化能解释

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("10 · 可观测与评估")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
