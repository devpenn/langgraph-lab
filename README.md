# langgraph-lab · LangGraph 及周边技术学习实验室

从零到能独立设计多 agent 系统：13 个递进小项目，毕业设计是把学习成果落回真实项目——用 LangGraph 重建 ding-local-bot 的大脑。

## 设计原则

1. **项目驱动**：每阶段一个可运行的小东西，概念在做中学；每阶段有验收清单，全勾才进下一阶段。
2. **零新账号零新凭证**：全程复用现有 Anthropic 兼容中转（glm-5.3-flash），与 ding-local-bot 的 claude CLI 同源配置。
3. **重原理轻框架**：先手写（ReAct 循环、审批门），再用官方预制件对比，知其所以然。

## 环境搭建

前置：uv（已装）、Python 由 uv 自动管理。

```bash
cp .env.example .env    # 值从 ~/.claude/settings.json 的 env 字段抄
uv sync
uv run python stages/00-hello-llm/verify.py   # 两步全绿即环境就绪
```

## 路线总览

| 阶段 | 主题 | 你将构建 | 时长 |
|---|---|---|---|
| [00](stages/00-hello-llm/) | 环境与模型链路 | 端点验证脚本 | 0.5h |
| [01](stages/01-langchain-basics/) | LangChain 基石 | 结构化抽取 + 工具调用 CLI | 2~3h |
| [02](stages/02-graph-fundamentals/) | 图的第一性原理 | 翻译-润色-审校流水线 | 3h |
| [03](stages/03-react-agent/) | ReAct Agent | 手写 agent ⇄ tools 循环 | 3~4h |
| [04](stages/04-persistence-memory/) | 持久化与记忆 | 断点续聊 + 跨会话偏好记忆 | 3h |
| [05](stages/05-human-in-the-loop/) | 人在回路 interrupt | 危险命令审批门 | 2~3h |
| [06](stages/06-streaming-async/) | 流式与异步 | 打字机输出 + 自定义进度事件 | 2~3h |
| [07](stages/07-multi-agent/) | 多智能体 | supervisor 编辑部（并行子图） | 4~5h |
| [08](stages/08-rag/) | RAG | 本仓库问答 agent（两种架构对比） | 3~4h |
| [09](stages/09-mcp/) | MCP | 本地工具 + MCP 工具混挂 | 2h |
| [10](stages/10-observability/) | 可观测与评估 | trace 定位 + 用例集跑分 | 2h |
| [11](stages/11-deployment/) | 部署为服务 | langgraph dev + curl 全流程 | 3h |
| [99](stages/99-capstone-bot/) | 毕业设计 | 重建 ding-local-bot 大脑 | 1~2 天 |

正式学习约 30~35 小时（不含毕业设计），按每天 1~1.5 小时约一个月走完。

## 每阶段怎么学（固定节奏）

1. **读（30%）**：读该阶段 README 的概念清单 + 对应官方文档。这个生态迭代快，中文资料常滞后，以官方文档为准；本 README 里的导入路径如报 ImportError，先查官方 quickstart 确认当期写法。
2. **做（50%）**：完成动手项目。卡壳先自己调 20 分钟，再查文档或问 AI。
3. **验（20%）**：过验收清单，把踩的坑记进 [notes/](notes/)。跑完不用复制终端输出——所有脚本运行会自动写入 [logs/lab.log](logs/lab.log)（见下「运行日志」），直接让 AI 读该文件复盘。

## 运行日志（lablog）

每个阶段脚本开头调用 `from lablog import start; start("NN · 主题")`，之后所有 print 与报错堆栈照常显示在终端，同时追加到 [logs/lab.log](logs/lab.log)（按时间分节，`logs/` 已 gitignore）。写法见各阶段 README 的「日志约定」。

## 技术覆盖地图

- **模型接入**：Anthropic 兼容协议 / ChatAnthropic / 流式 —— Stage 0、1、6
- **LangChain 核心**：消息 / 结构化输出 / 工具调用 / LCEL —— Stage 1
- **LangGraph 核心**：State / reducer / 边 / subgraph / Send / Command —— Stage 2、6、7
- **Agent 模式**：ReAct / ToolNode / 多 agent（supervisor、handoff）—— Stage 3、7
- **持久化**：checkpointer / thread / time travel / Store 长期记忆 —— Stage 4
- **人在回路**：interrupt / Command(resume) —— Stage 5、11
- **RAG**：切块 / embedding / 向量库 / agentic RAG —— Stage 8
- **MCP**：adapters / stdio server —— Stage 9
- **可观测与评估**：LangSmith / Langfuse / eval —— Stage 10
- **部署**：langgraph dev / threads-runs API —— Stage 11
- **工程**：uv 依赖分组 / 项目结构 —— 全程

## 与 ding-local-bot 的关系

Stage 99 是毕业设计：用这套知识重写现有机器人的大脑（连接层不动、行为对齐、增强审批与进度推送），学完即用上，用上即巩固。对应关系见 [stages/99-capstone-bot/](stages/99-capstone-bot/)。
