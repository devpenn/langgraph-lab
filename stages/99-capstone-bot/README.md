# Stage 99 · 毕业设计：重建 ding-local-bot 的大脑（1~2 天）

把整条学习路线落回真实项目：用 LangGraph 重写机器人的「大脑」，连接层行为对齐现有 bash 版，**telegram 渠道先行**（有冒烟测试、不影响线上钉钉）。代码建议独立于本 lab 放进 ding-local-bot 仓库新目录（如 `langgraph/`）。

## 学习 → 实战对应表

| 学习阶段 | 落到机器人里的什么 |
|---|---|
| 04 持久化 | SqliteSaver + thread_id 替代「会话文件 + --resume + TTL」 |
| 02/07 图结构 | gate → preprocess → agent ⇄ tools → reply 主图 |
| 03 工具 | bash 白名单工具 / 读写文件 / `run_claude_cli` 兜底工具 |
| 05 interrupt | 高危命令 IM 审批（替代 --dangerously-skip-permissions 裸奔） |
| 06 流式 | 任务进度推送到 IM（替代全程静默） |
| 08 RAG（可选） | 动手前先查本机 dev-knowledge |

## 里程碑

- **M1 CLI 版**：消息进出都走终端，图全绿（守门 / 会话复用 / 工具 / 审批）
- **M2 接 telegram**：Python 重写 getUpdates 轮询（长轮询 + socks5 代理，对齐 bash 版行为），图接管 reply
- **M3 审批与进度**：interrupt → sendMessage 询问，回复 y/n 后 resume；custom 事件推送进度
- **M4 验收对比**：同一批任务分别打旧 bash 版和新版，写行为差异报告

## 上线标准

- smoke-test 全绿；白名单外消息 fail-closed
- 重启后会话可续（SqliteSaver 落盘）；危险命令必拦截
- 稳定跑一周后，再考虑钉钉渠道迁移（dws dev connect 的 agent-cmd 换成新版入口即可）

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("99 · 毕业设计")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
