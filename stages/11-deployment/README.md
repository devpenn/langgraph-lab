# Stage 11 · 部署为服务（3h）

```bash
uv sync --extra server   # 装 langgraph-cli[inmem]
```

## 核心概念

- **langgraph.json**：声明图入口 → `langgraph dev` 起本地服务（自带 Studio 可视化调试界面）
- **REST 抽象**：threads（会话）→ runs（一次执行）→ stream（事件流）；checkpointer 自动升级为服务端持久化，thread_id 归服务管
- **interrupt 也能过 API**：run 挂起 → 从 threads/{id}/history 看到 `__interrupt__` → POST resume
- 后台 runs / cron 是 LangGraph Server 的进阶项，了解即可

## 动手项目：服务化审批 agent（本目录 + 根目录 langgraph.json）

1. 把 Stage 5 的审批 agent 注册进 `langgraph.json`，`langgraph dev` 跑起来
2. **纯 curl** 走完全流程：建 thread → 发消息 → 收到 interrupt → resume → 拿最终回复
3. 在 Studio 里可视化跑一遍同样的流程，对照 curl 的请求

## 验收清单

- [ ] 外部进程（curl / 另一个终端）能驱动一次带 interrupt 的完整会话
- [ ] 能说清「服务化之后，checkpointer 和 thread_id 归谁管了」

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("11 · 部署为服务")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
