# Stage 7 · 图的进阶形态与多智能体（4~5h）

## 核心概念

- **Subgraph**：图套图。子图可与父图共享 state schema，也可自带 schema（边界做字段映射）——多 agent 的 state 隔离靠它
- **Send API**：条件边返回 `Send(node, state)` 列表 → 动态并行 n 路（map-reduce）。与「写死多个分支」的本质区别：分支数运行时才知道
- **`Command(goto=...)`**：节点内部直接决定去哪，可与 state 更新一起返回
- **多 agent 拓扑**：supervisor（中心调度）/ handoffs（去中心转交）/ 群聊式；官方 `langgraph-supervisor`、`langgraph-swarm` 库可对照学习

## 动手项目：编辑部（代码写在 `07/`）

- supervisor 收到选题 → **Send 派 2 个研究员并行调研**（各自子图，state 独立）→ reducer 汇总 → 写手成稿 → 审稿人 pass / 打回（打回带意见回写手，最多 2 轮）
- 每个角色：独立 system prompt + 私有工具集

## 验收清单

- [ ] 画出完整拓扑（含 Send 并行部分），贴进 notes
- [ ] 说清父图与子图的 state 边界：子图改了同名 key 会怎样？
- [ ] 解释 Send 和普通条件边的区别，以及什么需求只能用 Send

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("07 · 多智能体")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
