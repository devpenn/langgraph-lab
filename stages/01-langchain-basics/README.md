# Stage 1 · LangChain 基石（2~3h）

LangGraph 的图节点里跑的就是 LangChain 的消息/模型/工具对象，这一阶段补齐地基。

## 核心概念

- **消息类型**：`SystemMessage` / `HumanMessage` / `AIMessage` / `ToolMessage`。模型 API 无状态，所谓「对话」就是把历史消息数组整个传过去
- **结构化输出**：`llm.with_structured_output(某个Pydantic模型)`——LLM 输出从「文本」升级成「可编程对象」
- **工具调用往返**（agent 的原子操作，务必手写一遍）：
  `@tool` 定义 → `llm.bind_tools([...])` → 返回的 AIMessage 带 `tool_calls` → 你执行函数 → 结果包成 ToolMessage 回传 → 再调一次模型得到最终回答
- **LCEL 够用即可**：`|` 管道把 Runnable 串起来（如 `prompt | llm`）

## 示例代码导读（按顺序跑）

| 文件 | 内容 | 对应知识点 |
|---|---|---|
| [common.py](common.py) | 共用配置：读 .env 建 llm + text_of 工具函数 | 所有示例的底座 |
| [ex1_messages.py](ex1_messages.py) | 两轮对话演示「无状态 + 全量历史」 | 消息类型 |
| [ex2_structured.py](ex2_structured.py) | 自由文本抽成 Event 对象 | 结构化输出 |
| [ex3_tool_roundtrip.py](ex3_tool_roundtrip.py) | 手写一次工具调用往返（核心） | 工具调用协议 |
| [assistant.py](assistant.py) | CLI 小助手，两个分支 | 动手项目 |

运行（项目根目录）：`uv run python stages/01-langchain-basics/ex1_messages.py`，其余同理。每个文件末尾有「课后实验」，做完再进下一个。assistant.py 是交互式的，直接运行后按提示输入。

## 动手项目：CLI 小助手（代码写在 `01/` 目录）

1. 输入一段自由文本（如「下周三下午和王总开会」），用 with_structured_output 抽成 `Event{title, date, time, participants}`
2. 注册一个假的 `get_weather(city)` 工具，问天气时观察模型发起 `tool_calls`，你回传固定值，模型给出最终回答
3. 实现两个分支：模型要调工具 / 不调直接回答——这就是 Stage 3 条件边的雏形

## 验收清单

- [ ] 不查文档能画出工具调用一次往返的消息流（Human → AI(tool_calls) → Tool → AI）
- [ ] 试一下 structured output 字段类型写错时会发生什么，记进 notes
- [ ] 能解释为什么模型 API 必须每次传完整历史

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("01 · LangChain 基石")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
