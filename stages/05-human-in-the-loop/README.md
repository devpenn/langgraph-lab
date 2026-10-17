# Stage 5 · 人在回路 interrupt（2~3h）

你的机器人现在靠 `--dangerously-skip-permissions` 裸奔。这一课给它装刹车，也是毕业设计的核心能力。

## 核心概念

- **`interrupt(payload)`**：节点内暂停整个图；state 已被 checkpointer 存档，进程可以直接退出
- **`Command(resume=value)`**：带着人的答复从暂停点继续；恢复后 `interrupt()` 的返回值就是 value
- **前提**：必须配 checkpointer（暂停 = 靠存档活着）
- **语义**：resume 后图从 interrupt 的**下一行**继续，不是重跑节点——所以节点要设计成幂等

## 动手项目：审批门（代码写在 `05/`）

1. 给 Stage 3 的 `run_cmd` 套一层 gate：命令命中危险词（rm / sudo / curl|sh / mv 到系统路径）→ `interrupt` 把命令展示出来，终端等 y/n
2. n → 跳过执行，给模型一条「用户已拒绝」的 ToolMessage 让它换方案；y → 放行
3. 两段式体验：第一次 `invoke` 挂起（进程可退出），之后单独一次 `invoke(Command(resume="y"), config)` 继续

## 思考题

- 挂起期间服务重启了，恢复后从哪继续？（用 get_state 亲自看看）
- 一个节点里有两个 `interrupt()`，resume 值怎么对应？（了解 interrupt 的 index 机制）

## 验收清单

- [ ] 拦截、放行、拒绝三条路都跑通
- [ ] 能画出「invoke → 挂起 → resume」两次调用之间发生了什么
- [ ] 把审批输出格式化成将来能塞进 IM 消息的样子（为毕业设计铺路）

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("05 · 人在回路 interrupt")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
