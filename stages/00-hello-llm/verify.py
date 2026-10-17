"""Stage 0 端点验证：确认能通过现有中转端点调用模型（非流式 + 流式）。

优先读 .env；没配则兜底读 ~/.claude/settings.json（与 claude CLI / ding-local-bot 同源）。
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("00 · 环境与模型链路")

from dotenv import load_dotenv

load_dotenv()


def _from_claude_settings() -> tuple[str, str]:
    path = Path.home() / ".claude" / "settings.json"
    if not path.exists():
        return "", ""
    env = json.loads(path.read_text()).get("env", {})
    return env.get("ANTHROPIC_BASE_URL", ""), env.get("ANTHROPIC_AUTH_TOKEN", "")


BASE_URL = os.getenv("ANTHROPIC_BASE_URL") or _from_claude_settings()[0]
API_KEY = os.getenv("ANTHROPIC_AUTH_TOKEN") or _from_claude_settings()[1]
MODEL = os.getenv("ANTHROPIC_MODEL", "glm-5.3-flash")

if not BASE_URL or not API_KEY:
    raise SystemExit(
        "缺少 ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN："
        "请填 .env（参考 .env.example），或确认 ~/.claude/settings.json 存在"
    )

# 环境检查通过后再导入，报错信息更聚焦
from langchain_anthropic import ChatAnthropic


def text_of(content) -> str:
    """只提取 text 块。glm 系模型会带 thinking 块（原始 content 是 block 列表），
    这是 Stage 1 会正式讲的消息结构，这里先见个面。"""
    if isinstance(content, str):
        return content
    return "".join(
        b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
    )


llm = ChatAnthropic(model=MODEL, base_url=BASE_URL, api_key=API_KEY, max_tokens=1024)

print(f"[1/2] 端点 {BASE_URL}  模型 {MODEL}")
# reply = llm.invoke("用一句话介绍 LangGraph 是什么。")
# print(f"[1/2] 非流式回复：{text_of(reply.content)}")
# print(f"[1/2] 用量：{getattr(reply, 'usage_metadata', {})}")

# print("[2/2] 流式输出：", end="")
# for chunk in llm.stream("从 1 数到 5，用顿号分隔，不要输出其他内容。"):
#     print(text_of(chunk.content), end="", flush=True)

reply = llm.invoke("现在几点了。")
print(f"[3/1] 非流式回复：{text_of(reply.content)}")
print(f"[3/2] 用量：{getattr(reply, 'usage_metadata', {})}")

for chunk in llm.stream("这是新的会话吗？有之前的记忆吗？两个问题分开回答，不要输出其他内容"):
    print(text_of(chunk.content), end="", flush=True)

print("\n✅ Stage 0 通过：模型端点可用，环境就绪")
