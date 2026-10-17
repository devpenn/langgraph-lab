"""动手项目：CLI 小助手 —— 会抽日程 + 会查（假）天气，README「动手项目」的完整实现。

运行方式（在项目根目录）：
    uv run python stages/01-langchain-basics/assistant.py

两种用法：
    记事：下周三下午三点和王总开会     ← 以「记事：」开头 → 走结构化抽取分支
    上海天气怎么样？                  ← 其他任意输入 → 走聊天 + 工具调用分支
    q                                 ← 退出

重点看主循环里的判断：模型回复带不带 tool_calls，走不同分支——
这个 if/else 就是 Stage 3 条件边（conditional edge）的雏形。
"""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("01 · CLI 小助手")

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from common import llm, text_of


# ============ 第一部分：结构化抽取（分支 A 用） ============

class Event(BaseModel):
    """从一段文字里抽出来的日程事件。"""

    title: str = Field(description="事件标题，比如「和王总开会」")
    date: str = Field(description="日期，尽量用 YYYY-MM-DD 格式，推不出来就写 unknown")
    time: str = Field(description="时间，HH:MM 格式，推不出来就写 unknown")
    participants: list[str] = Field(description="参与人姓名列表，没有就给空列表")

def do_event(context: str) -> Event:
    return llm.with_structured_output(Event).invoke(context)# type: ignore[return-value]

@tool
def get_weather(city: str) -> str:
    """城市的天气、温度查询"""
    return f"{city}: 晴,30度"

llm_with_tools = llm.bind_tools([get_weather])

history = [SystemMessage(content="你是一个简单直接的中文回复助手")]
print("CLI 小助手已启动（输入 q 退出）")
print('试试：「记事：下周三下午三点和王总开会」 或 「上海天气怎么样？」')

while True:  # 无限循环，直到遇到 break
    try:
        user_input = input("\n你> ").strip()  # input() 读一行键盘输入，strip() 去首尾空白
    except EOFError:  # Ctrl+D 或没有输入可读时退出
        print("强制退出！")
        break

    if user_input.lower() in ("q", "quit", "exit"):
        print("再见！")
        break
    if not user_input:  # 空输入，重新问
        continue

    today = date.today()
    weekday = "一二三四五六日"[today.weekday()]
    today_line = f"今天是 {today:%Y-%m-%d} 周{weekday}。"
    history.append(HumanMessage(content=today_line + user_input))

    if user_input.startswith("记事"):
        event = do_event(user_input)
        # Event 对象模型读不懂，转成一句人话写回历史，后续对话才能「记得」
        history.append(AIMessage(
            content=f"已记录日程：{event.title}，时间 {event.date} {event.time}，"
                    f"参与人：{'、'.join(event.participants)}"
        ))
        print(f"助手>:\n")
        print(f"事件标题：{event.title}")
        print(f"日期：{event.date} {event.time}")
        print(f"人员：{event.participants}")
        continue

    while True:
        # {"name": "foo", "args": {"a": 1}, "id": "123"}
        reply = llm_with_tools.invoke(history)
        history.append(reply)
        tool_calls = reply.tool_calls
        if not tool_calls:
            print(f"助手>:\n")
            print(text_of(reply.content))
            break

        for tool_call in tool_calls:
            print(f"call tool：{tool_call['name']} {tool_call['args']} {tool_call['id']}")
            tool_call_result = get_weather.invoke(tool_call['args'])
            history.append(ToolMessage(
                tool_call_id=tool_call['id'],
                content=tool_call_result
            ))
