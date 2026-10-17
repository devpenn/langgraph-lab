# Stage 3 · 手写 ReAct Agent（3~4h）

LangGraph 的灵魂模式：模型节点 ⇄ 工具节点循环。写完这个，市面上 80% 的「agent 框架」对你不再神秘。

## 核心概念

- **agent 节点**：`llm.bind_tools(tools).invoke(state["messages"])`，`add_messages` reducer 自动追加
- **条件边**：最后一条消息有 `tool_calls` → 去 tools 节点；没有 → END
- **ToolNode**：批量执行 tool_calls、自动包 ToolMessage、自带错误处理
- **先手写再用预制件**：官方入口（langchain 1.x 为 `langchain.agents.create_agent`，以当期文档为准）对比差异

## 动手项目：本机小助手（代码写在 `03/`）

- 工具三件套：`read_file(path)`（限本仓库内）、`now()`、`run_cmd(cmd)`（白名单：ls / wc / date 等只读命令）
- 任务样例：「统计 stages 下所有 README 的总行数」「这个项目是干嘛的」

## 思考题

- 工具结果为什么必须以 ToolMessage 身份回传，而不是拼进 prompt 字符串？
- 模型一口气要调 3 个工具，ToolNode 是并行还是串行？
- 你的 agent 什么情况下会陷入死循环？加什么能止损？（提示：recursion_limit / state 里记步数）

## 验收清单

- [ ] 不看参考默写整张图（agent ⇄ tools）
- [ ] 读一遍 ToolNode 源码（就在 .venv 的 site-packages 里，百来行），说出它比你的手写版多处理了什么
- [ ] 用官方 create_agent 预制件重写一遍，行为等价

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("03 · ReAct Agent")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
