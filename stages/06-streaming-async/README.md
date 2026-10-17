# Stage 6 · 流式与异步（2~3h）

你的机器人任务执行全程静默、用户只能干等。这一课解决「过程可见」。

## 核心概念

- **四种 stream_mode**：`values`（每步全量 state）/ `updates`（每步增量）/ `messages`（LLM token 级）/ `custom`（自定义事件）
- **节点内发自定义事件**：`get_stream_writer()` 拿 writer，随 custom 模式流出（当期 API 以官方文档为准）
- **异步全家桶**：`async def` 节点、`ainvoke` / `astream`；工具是 IO 密集时异步才有真正收益
- stream mode 可在 compile 时配，也可 invoke 时传

## 动手项目：过程可见的聊天（代码写在 `06/`）

1. 打字机效果：messages 模式逐 token 打印最终回答
2. 工具进度：updates 模式显示「进入节点 xx」；custom 模式在工具执行前后发「开始执行 run_cmd: ls」
3. 把整个程序改成 async 版，用 `astream` 驱动

## 验收清单

- [ ] 一句话说出四种 stream_mode 各适合什么场景
- [ ] token 流里怎么区分「最终回答」和「工具调用前的思考」？（观察 chunk 里的 tool_calls 字段）
- [ ] async 版与同步版行为一致

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("06 · 流式与异步")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
