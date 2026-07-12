import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from graph import build_graph
from resources import RESOURCES

graph = build_graph()

print("------简易RAG加载完毕-----")

while True:
    question = input("请输入问题：")
    if question == "q":
        break
    if question == "":
        continue
    config = {"configurable": {"thread_id": "terminal_user"}}
    result = graph.invoke(
        {
            "question":question
        },
        config = config
    )
    print(result.get("answer","未生成答案"))
