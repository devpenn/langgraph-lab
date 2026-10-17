"""示例 2：结构化输出 —— 让 LLM 的回答从「一段文本」升级成「一个 Python 对象」。

运行方式（在项目根目录）：
    uv run python stages/01-langchain-basics/ex2_structured.py

场景：用户输入一段自由文本（「下周三下午和王总开会」），
程序拿到的是结构化的字段，可以直接存数据库、可以做逻辑判断。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("01 · ex2 结构化输出")

# ---- Pydantic：用 Python 类描述「我想要的数据长什么样」 ----
# class 定义一个类；(BaseModel) 表示继承 Pydantic 提供的基类。
# 类里每个属性就是一个字段，格式是：字段名: 类型 = Field(描述)
# Field 里的 description 会传给模型，帮它理解每个字段该填什么。
from pydantic import BaseModel, Field

from common import llm


class Event(BaseModel):
    """从一段文字里抽出来的日程事件。"""

    title: str = Field(description="事件标题，比如「和王总开会」")
    date: str = Field(description="日期，尽量用 YYYY-MM-DD 格式，推不出来就写 unknown")
    time: str = Field(description="时间，HH:MM 格式，推不出来就写 unknown")
    participants: list[str] = Field(description="参与人姓名列表，没有就给空列表")
    # 给了默认值的字段是「可选」的：模型不填也不报错（Pydantic 规则：
    # 没有默认值的字段 = 必填，模型漏填就直接 ValidationError）
    ori: str = Field(default="", description="非结构化的模型原始回复")


# with_structured_output(Event) 返回一个「新 llm」：
# 它的回答被强制约束成 Event 的格式，invoke 直接拿到 Event 对象。
extractor = llm.with_structured_output(Event)

text = "下周三下午三点和王总、李经理,还有我最尊敬、最喜欢、最帅的D哥在天安门城楼上开会聊季度复盘"
event = extractor.invoke(text)  # 注意：event 不是字符串，是一个对象！

# 对象的属性用「点号」访问：event.title、event.date …
print("输入文本:", text)
print("标题:  ", event.title)
print("日期:  ", event.date)
print("时间:  ", event.time)
print("参与人:", event.participants)  # list[str] 会打印成 ['王总', '李经理']
print("模型原始回复:", event.ori)

# 拿到对象之后就能写普通代码逻辑了，比如：
if event.time != "unknown":
    print(f"\n可以定闹钟了：{event.date} {event.time} 前提醒。")

# ==========================================================
# 你发现的现象：date=unknown，但其他字段都抽对了。为什么？
# 模型是无状态的——它不光没有对话记忆（ex1 的结论），连「今天是几号」
# 都不知道。「下周三」是相对日期，没有参照物就算不出来，只能按字段
# 说明老实填 unknown。
# 解决办法：把当前日期塞进提示词，给它参照物。真实系统都是这么干的。
# ==========================================================
from datetime import date

today = date.today()
weekday = "一二三四五六日"[today.weekday()]  # weekday() 返回 0~6，周一=0
today_line = f"今天是 {today:%Y-%m-%d} 周{weekday}。"

event2 = extractor.invoke(today_line + text)  # 同样的文本，前面加一行今天日期
print("\n--- 带上今天日期，再抽一次 ---")
print("提示词前缀:", today_line)
print("日期:  ", event2.date)
print("时间:  ", event2.time)

# ==========================================================
# 验收清单实验（第 2 条）：故意把类型写错，观察会发生什么
# 1. 把上面 date 的类型注解 str 改成 int：`date: int = Field(...)`
# 2. 重新运行本文件
# 3. 观察现象：是报错（Pydantic 校验失败）？还是模型硬把日期变成数字？
# 4. 把你看到的现象记进 notes/01-langchain-basics.md 的「踩过的坑」
# ==========================================================

print("\n✅ ex2 完成（别忘了做注释里的类型写错实验）")
