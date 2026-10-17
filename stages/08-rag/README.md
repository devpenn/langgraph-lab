# Stage 8 · RAG 检索增强（3~4h）

相关技术里最常用的一块：让 agent 拥有私有知识。

```bash
uv sync --extra rag   # 装 chromadb
```

## 核心概念

- **五步**：load（读文档）→ split（切块）→ embed（向量化）→ store（向量库）→ retrieve（相似度检索）
- **本地零外部服务**：Chroma（默认内置 embedding 模型，首次运行会自动下载）
- **两种架构**：
  - workflow 式：检索是固定节点（先查后答，必然查）
  - agentic 式：检索做成工具（模型自己决定查不查、查几次）
- **引用溯源**：检索结果带元数据（来源文件/位置），回答时标注

## 动手项目：本仓库问答（代码写在 `08/`）

1. 把本仓库所有 `*.md` 切块入库
2. 先做 workflow 式（固定：检索 → 生成）
3. 再做 agentic 式（`search_docs` 工具 + Stage 3 的 agent 骨架）
4. 对比两者在「这个问题需要查吗」上的行为差异

**关键实验**：把 chunk_size 调成 100 / 2000 各跑一遍，体会「检索质量 ≥ 模型能力」。

## 验收清单

- [ ] 两套架构都能跑，说出各自适用场景
- [ ] 回答错误时能定位坏在哪一层（切分 / embedding / 检索阈值 / 生成）
- [ ] 每个回答都带来源文件名

## 日志约定

本阶段脚本开头写：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # 项目根，便于导入 lablog
from lablog import start

start("08 · RAG")
```

之后所有 print 和报错照常显示在终端，同时自动追加到项目根的 logs/lab.log。
跑完不用复制输出，直接让 AI 读 logs/lab.log 即可复盘。
