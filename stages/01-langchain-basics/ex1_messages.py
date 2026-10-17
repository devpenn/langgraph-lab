"""示例 1：消息类型 —— 所谓「对话」，就是把消息数组整个传过去。

运行方式（在项目根目录）：
    uv run python stages/01-langchain-basics/ex1_messages.py

这个例子回答验收清单第 3 条：为什么模型 API 必须每次传完整历史？
因为它是「无状态」的——每次调用都是一次全新的请求，服务器不记得你。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("01 · ex1 消息类型")

# ---- 导入三种最常用的消息类型 ----
# SystemMessage: 设定身份/规则，用户「看不见」，永远放列表第一个
# HumanMessage:  用户说的话
# AIMessage:     模型之前的回答
from langchain_core.messages import HumanMessage, SystemMessage

from common import llm, text_of  # common.py 在本目录，提供配好端点的 llm

# ---- 组一个消息列表 ----
# 列表用方括号 []，元素之间逗号分隔；这里放的是两个消息对象。
messages = [
    SystemMessage(content="你是一个说话简短的助手，每次回答不超过两句话。"),
    HumanMessage(content="我叫小彭，最喜欢吃火锅。"),
]

# invoke = 发起一次完整往返，返回一个 AIMessage 对象
reply = llm.invoke(messages)
print("第一轮回复:", text_of(reply.content))

# ---- 第二轮：带上完整历史（用户消息 + 模型回复都留在列表里） ----
# append = 往列表末尾追加一个元素。
messages.append(reply)
messages.append(HumanMessage(content="我叫什么名字？最喜欢吃什么？"))

reply2 = llm.invoke(messages)
print("\n第二轮回复（带完整历史）:", text_of(reply2.content))

# ---- 对照实验：一模一样的问题，但不带任何历史 ----
# 只传这一句新问题，前面的 System/Human/AI 一概不给。
# API 无状态 → 模型此刻对你一无所知。
fresh = llm.invoke([HumanMessage(content="我叫什么名字？最喜欢吃什么？")])
print("同问题不带历史:  ", text_of(fresh.content))

# ==========================================================
# 课后实验：
# 1. 注释掉 `messages.append(reply)`，并把第二个问题换成
#    「你刚才反问了我一句什么？」再跑——模型答不上来了。
#    道理：你说过的话（第一条 HumanMessage）还在列表里，所以它记得
#    你的名字；但它「自己说过的话」没了。AI 的历史同样要靠你传！
#    （只注释 append 却继续问名字，模型照样知道——名字在你那条
#    HumanMessage 里，这个实验设计曾经是个坑，已修正为对照实验。）
# 2. 把 SystemMessage 里的「不超过两句话」改成「每次回答必须押韵」，
#    看看第一轮回复风格怎么变——SystemMessage 就是这么控制行为的。
# ==========================================================

print("\n✅ ex1 完成")
