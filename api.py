import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from fastapi import FastAPI
from pydantic import BaseModel
from graph import build_graph

class Question(BaseModel):
    question: str
    thread_id: str = "default"

class AnswerResp(BaseModel):
    answer: str

print("正在加载知识库和模型，请稍候...")
graph = build_graph()
print("服务已就绪！")

app = FastAPI(title = "React RAG Agent", version = "1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AnswerResp)
def ask(req:Question):
    config = {"configurable": {"thread_id": req.thread_id}}
    result = graph.invoke(
        {"question": req.question},
        config = config
    )
    return {"answer": result.get("answer", "未生成答案")}