# Stage 0 · 环境与模型链路（0.5h）

目标：跑通「本机 → Anthropic 兼容中转 → GLM 模型」的最短链路。后面所有阶段都建立在这条链路上。

## 做

1. `cp .env.example .env`，从 `~/.claude/settings.json` 的 env 字段抄 `ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN`
2. `uv sync`
3. `uv run python stages/00-hello-llm/verify.py`

## 理解

- `ChatAnthropic` 就是一个封装了 HTTP 调用的 Runnable：`invoke`（一次完整往返）、`stream`（逐 chunk 吐出）
- `base_url` + `api_key` 决定打到哪、用什么身份；`model` 决定用哪个模型
- 你的 ding-local-bot 里 claude CLI 用的就是同一组配置——CLI 没有魔法，和 SDK 走的是同一套 HTTP 协议

## 验收清单

- [ ] verify.py 两步全绿（非流式 + 流式）
- [ ] 改造 verify.py：问两个不同的问题，并打印 token 用量（`response.usage_metadata`）
- [ ] 能用自己的话说出 invoke 和 stream 的区别，以及什么场景用哪个

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("00 · 环境与模型链路")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
