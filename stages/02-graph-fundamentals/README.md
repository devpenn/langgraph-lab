# Stage 2 · LangGraph 第一性原理（3h）

一切 LangGraph 程序的地基：状态、节点、边、reducer。

## 核心概念

- **StateGraph + State**：图的状态就是一个 TypedDict / Pydantic 对象；每个节点是「state 进 → 返回局部更新出」的函数
- **Reducer**：同名 key 的更新如何合并。默认 = **覆盖**；`Annotated[list, add_messages]` / `operator.add` = 追加。初学者 90% 的 bug 出在对 reducer 的误解
- **边**：普通边（固定下一跳）、条件边（路由函数算下一跳）、START / END
- **compile()** 后得到 Runnable，invoke / stream 都能用；`graph.get_graph().draw_mermaid()` 可视化

## 动手项目：翻译流水线（代码写在 `02/`）

1. 节点：translate（中→英）→ polish（润色）→ review（审校，输出 pass / fix + 意见）
2. review 不过走条件边打回 polish；state 里记轮数，**最多 2 轮强制 END**——想想为什么不能无限打回
3. 把 `draw_mermaid()` 输出贴在代码注释里

## 关键实验（比项目本身更重要）

- 把 polish 的返回从 `{"text": ...}` 改成返回整个 state，观察覆盖行为
- 故意给一个 list key 不加 `Annotated` reducer，让数据丢一次，再修好

## 验收清单

- [ ] 能说清「节点返回值」和「state 更新」的关系
- [ ] 条件边的路由函数返回什么？它怎么决定下一跳？
- [ ] mermaid 图贴好了，能给别人讲一遍你的图

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("02 · 图的第一性原理")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
