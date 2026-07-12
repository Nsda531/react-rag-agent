from agent import agent_node
from tool_node import tool_node
import json
from graph import build_graph

app = build_graph()

def run(question):
    state = {
        "question": question,
        "messages":[],
        "action":"",
        "action_input":"",
        "observation":"",
        "answer":""
    }
    result = app.invoke(state)
    return result["answer"]
    
