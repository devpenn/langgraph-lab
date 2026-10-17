"""本阶段共用配置：读取端点配置，创建 llm 对象，供各示例文件导入。

其他示例里写 `from common import llm` 就能拿到配好端点的模型对象。
这样端点配置只写一遍，示例文件里只剩真正的知识点。
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()  # 读取 .env（会从当前目录向上层目录找，所以能找到项目根的 .env）


def _from_claude_settings() -> tuple[str, str]:
    """兜底方案：.env 没配时，直接读 claude CLI 的配置文件（同一组凭证）。"""
    path = Path.home() / ".claude" / "settings.json"
    if not path.exists():
        return "", ""
    env = json.loads(path.read_text()).get("env", {})
    return env.get("ANTHROPIC_BASE_URL", ""), env.get("ANTHROPIC_AUTH_TOKEN", "")


BASE_URL = os.getenv("ANTHROPIC_BASE_URL") or _from_claude_settings()[0]
API_KEY = os.getenv("ANTHROPIC_AUTH_TOKEN") or _from_claude_settings()[1]
MODEL = os.getenv("ANTHROPIC_MODEL", "glm-5.3-flash")

if not BASE_URL or not API_KEY:
    raise SystemExit("缺少 ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN，参考 .env.example")

# ChatAnthropic 就是一个「可以对话的对象」。
# max_tokens 限制单次回复的最大长度，避免偶发的超长回答拖慢实验。
llm = ChatAnthropic(model=MODEL, base_url=BASE_URL, api_key=API_KEY, max_tokens=1024)


def text_of(content) -> str:
    """从模型回复里提取纯文本。

    为什么需要它：glm 系模型返回的 content 有时不是字符串，
    而是一个「块列表」——里面混着 thinking 块（思考过程）和 text 块（正文）。
    这个函数只把 text 块拼出来。Stage 0 的 verify.py 里你见过它了。
    """
    if isinstance(content, str):
        return content
    return "".join(
        b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"
    )
