# ReAct RAG Agent
基于 **LangGraph + ChromaDB + Redis + Ollama** 的本地React智能问答Agent

## 架构
```
    用户输入（HTTP/终端）
            │
            ▼
      ┌───────────┐
      │   agent   │◄────────────┐
      └─────┬─────┘             │
            │                   │
            ▼                   │
      ┌───────────┐             │
      │   route   │             │
      └─────┬─────┘             │
            │                   │
   "finish" │ "rag" / "weather" / ...            
     ┌──────┼──────┐            │
     ▼             ▼            │
   ┌────┐      ┌──────┐         │
   │END |      │ tool │─────────┘
   └────┘      └──────┘  observation
   返回答案               带回 agent
            │
            ▼
工具层 (registry 可插拔)
├── rag          知识库检索 (ChromaDB)
├── weather      天气查询 (wttr.in)
├── web_search   网页搜索 (DuckDuckGo)
└── calculator   数学计算
Redis 会话记忆 ── 多轮对话上下文持久化
```

## 特性

- 🤖 **ReAct 自主推理** — Agent 思考后决定调用哪个工具或直接回答
- 📚 **RAG 检索增强** — ChromaDB 持久化向量库，一次建库永久复用
- 🔧 **多工具协作** — 知识库检索、天气查询、网页搜索、数学计算
- 💬 **多轮对话记忆** — Redis checkpoint，会话上下文跨轮持久化
- 🔌 **可插拔工具系统** — registry 模式，新工具一个文件搞定
- 🏠 **全本地运行** — Ollama + SentenceTransformer，不调云端 API
- 🌐 **HTTP API** — FastAPI + Swagger 自动文档，网页可交互


## 技术栈
| 层 | 技术 |
|-----|-----|
| Agent 编排 | LangGraph + StateGraph |
| 大模型 | Ollama + qwen3:4b |
| Embedding | SentenceTransformer + all-MiniLM-L6-v2 |
| 向量数据库 | ChromaDB(持久化) |
| 会话记忆 | Redis + langgraph-checkpoint-redis |
| 文档解析 | PyPDF |
| Web服务 | FastAPI + Uvicorn |
| 工具 | wttr.in / DuckDuckGo / eval |

## 快速开始
### 1.环境准备

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/Scripts/activate   #Windows
# .venv/bin/activate            # Mac/Linux

# 安装依赖
pip install -r requirements.txt

# 安装并启动 Ollama,拉取模型
ollama pull qwen3:4b

# 启动Redis（需要Docker）
docker run -d --name redis-rag -p 6379:6379 redis/redis-stack:latest
```

### 2.准备知识库PDF
将 PDF 文件放入 data/ 目录，默认读取 data/午餐科学搭配与食谱大全.pdf。

### 3.启动服务
```
# HTTP API 模式
uvicorn api:app --reload

# 终端交互模式
python main.py
```

### 4.调用
```
# curl
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "午餐怎么搭配？", "thread_id": "user_1"}'

# 或访问 Swagger 页面
http://localhost:8000/docs
```

## 多轮对话
同一个 thread_id 共享会话记忆：
```bash
curl -X POST ... -d '{"question": "北京天气如何？", "thread_id": "user_1"}'
curl -X POST ... -d '{"question": "那明天呢？", "thread_id": "user_1"}'
```
Agent 记得上一轮说的是北京

## 添加新工具
1. 在 tools/ 目录新建Python文件
2. 函数签名：def my_tool(state,resources):
3. 在 tools/registry.py 注册
```python
**tools/my_tool.py**
def my_tool(state,resources):
    state["observation"] = "工具结果"
    return state
```

```python
**tools/registry.py**
TOOLS["my_tool"] = {
    "function": my_tool,
    "description": "工具描述"
}
```

## 项目结构
```
.
├── main.py                                     # 终端交互入口
├── api.py                                      # FastAPI HTTP 服务
├── agent.py                                    # ReAct Agent (prompt + 决策)
├── graph.py                                    # LangGraph 图谱编排
├── tool_node.py                                # 工具调度中心
├── state.py                                    # 状态定义
├── llm.py                                      # Ollama 调用封装
├── embedding.py                                # 知识库构建 (ChromaDB)
├── retrieval.py                                # 向量检索
├── resources.py                                # 资源管理（懒加载知识库）
├── tools/
│   ├── registry.py                             # 工具注册表
│   ├── rag.py                                   # RAG检索工具
│   ├── weather.py                              # 天气查询工具
│   ├── web_search.py                           # 网页查询工具
│   ├── calculator.py                           # 计算器工具
├── data/
│   ├── *.pdf                                   # 知识库 PDF
│   ├── chroma_db/                              # ChromaDB 持久化文件
└── requirements.txt
```

## License
MIT