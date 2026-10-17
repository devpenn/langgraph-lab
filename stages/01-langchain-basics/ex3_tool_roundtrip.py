"""示例 3：手写工具调用往返 —— agent 的原子操作，每一行都要看懂。

运行方式（在项目根目录）：
    uv run python stages/01-langchain-basics/ex3_tool_roundtrip.py

一次完整往返的消息流（验收清单第 1 条要你合上文档默画的图）：

    HumanMessage("北京天气怎么样？")
        │  第 1 次 invoke（请求 = 问题 + 工具说明书，模型二选一）
        ▼
    ┌── 判断分支：reply.tool_calls 是否为空？（分支必须挂在这里！）
    │
    ├─ 非空 → 模型「点菜」，正文通常为 ''
    │     你执行工具 → ToolMessage 回传 → 第 2 次 invoke → 最终回答
    │
    └─ 空 → 模型直接回答，reply.content 就是答案，不需要第 2 次 invoke

为什么分支不能挂在正文上：模型点菜时正文往往是空字符串——它的输出
「话费」全花在发起调用了。所以判断依据只能是 tool_calls，永远别猜 content。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("01 · ex3 工具调用往返")

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

from common import llm, text_of


# ---- 定义工具 ----
# @tool 是「装饰器」：把普通函数包装成模型能理解的工具对象。
# docstring 和类型注解会被打包进「工具说明书」，随每次请求发给模型。
@tool
def get_weather(city: str) -> str:
    """查询指定城市今天的天气，返回一句话描述。"""
    return f"{city}：晴，28 度"


# 把工具绑给模型：之后的每次请求都会带上工具说明书。
# 注意：模型只拿到说明书，它不会执行函数——函数只存在于你的进程里。
llm_with_tools = llm.bind_tools([get_weather])


def round_trip(question: str) -> None:
    """跑一次完整往返。分支挂在 tool_calls 上：有 → 走工具流程；无 → 直接回答。"""
    print(f"\n{'=' * 20} 问：{question} {'=' * 20}")
    messages = [HumanMessage(content=question)]

    # ---- 第 1 次调用：模型二选一（说正文 / 点菜）----
    reply = llm_with_tools.invoke(messages)
    messages.append(reply)  # 无论哪个分支，这条 AIMessage 都必须进历史

    # ================= 分支 B：没点菜 → 直接就是答案 =================
    if not reply.tool_calls:  # 空列表 [] 在 if 里就是 False
        print("【直接回答分支】", text_of(reply.content))
        return  # return = 函数到此结束，不需要第 2 次调用

    # ================= 分支 A：点菜了 → 执行 → 回传 → 再问 =================
    # 走到这里时正文往往是 ''，这是正常的，不是出错。
    for tool_call in reply.tool_calls:
        # tool_call 是字典：name=工具名 args=模型填的参数 id=点菜编号
        print("【工具分支】模型点菜:", tool_call["name"], tool_call["args"])
        result = get_weather.invoke(tool_call["args"])  # 你来执行（模型执行不了）
        print("【工具分支】执行结果:", result)
        messages.append(ToolMessage(
            content=result,               # 工具返回值
            tool_call_id=tool_call["id"],  # 和点菜编号配对，删掉会报错
        ))

    # ---- 第 2 次调用：模型看到工具结果，给出最终回答 ----
    final = llm_with_tools.invoke(messages)
    print("【工具分支】最终回答:", text_of(final.content))


# 同一段代码跑两个问题，亲眼看到两个分支各走一次：
round_trip("北京今天天气怎么样？适合穿短袖吗？")  # 该走工具分支
round_trip("1 加 1 等于几？用一句话回答。")       # 该走直接回答分支

# ==========================================================
# 课后实验：
# 1. 问「北京和上海哪个更热？」——观察模型会不会一次点两道菜
#   （tool_calls 列表里两个元素，for 循环各执行一遍）。
# 2. 把 ToolMessage 的 tool_call_id 参数删掉再跑，看报什么错——
#   理解「结果要和点菜编号配对」的意义。现象记进 notes。
# ==========================================================

print("\n✅ ex3 完成")
