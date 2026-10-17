# Stage 9 · MCP 接入（2h）

```bash
uv sync --extra mcp   # 装 langchain-mcp-adapters
```

## 核心概念

- **MCP = 工具生态的标准插座**：任何 MCP server 的能力都变成你 agent 的工具，不必自己写
- **架构**：client（你的程序）↔ server（stdio 子进程或 HTTP），server 暴露 tools / resources / prompts
- **langchain-mcp-adapters**：`MultiServerMCPClient` 把 MCP server 的 tools 转成 LangChain 工具，喂给 `bind_tools`

## 动手项目：混挂工具的 agent（代码写在 `09/`）

1. 用 `uvx` 起官方 filesystem MCP server（限定本仓库目录）
2. agent 同时挂：Stage 3 的本地 `run_cmd` + MCP 的文件工具
3. 问「项目里哪个 stage 的 README 最长」，观察模型选了哪边的工具

## 思考题

- MCP 工具和普通 `@tool` 在模型眼里有区别吗？（没有——对模型都一样是 tool）
- 什么场景值得把能力包成 MCP server 而不是本地函数？（跨进程 / 跨语言 / 复用给别的 agent）

## 验收清单

- [ ] 混挂工具的 agent 正常工作
- [ ] 能指出 tools/list、tools/call 两个 RPC 发生在你调用链的哪一步

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("09 · MCP")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
