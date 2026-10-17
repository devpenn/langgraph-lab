# Stage 4 · 持久化与记忆（3h）

ding-local-bot 里手写的「会话文件 + --resume + TTL」就是本课内容的原始形态。学完你会明白那套 hack 对应的正规解法。

## 核心概念

- **Checkpointer**：图每执行一步就把 state 存档。`MemorySaver`（内存）→ `SqliteSaver`（落盘，进程重启可续）
- **thread_id**：一次对话的身份证。同 thread = 续聊，换 thread = 新会话——你 /tmp 下那个 sessions 文件干的就是这事
- **内省**：`graph.get_state(config)` 看当前状态，`graph.get_state_history(config)` 看全部存档历史
- **Time travel**：取旧 checkpoint 的 config 再 invoke，从那个时刻重放
- **跨线程长期记忆**：`BaseStore` / `InMemoryStore`，`put/get/search`，与 thread 无关——「用户偏好」这类知识放这里

## 动手项目：能断点续聊的 CLI（代码写在 `04/`）

1. CLI 聊天，`--thread` 参数选会话；kill 进程重启后，同 thread 接着聊
2. `/history` 看当前 thread 的 checkpoint 历史；`/travel N` 回到第 N 步重放
3. 偏好记忆：聊到「我用 vim 不用 emacs」时存进 Store；**换一个 thread** 问「我喜欢哪个编辑器」能答对

## 验收清单

- [ ] 杀进程重启后续聊成功
- [ ] time travel 重放一次，并说出 checkpoint 里存了什么
- [ ] 能说清 checkpointer（短期、thread 内）与 Store（长期、跨 thread）的分工

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("04 · 持久化与记忆")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
