from typing import TypedDict,Any
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.redis import RedisSaver
from agent import agent_node
from tool_node import tool_node
from state import State

def route(state:State):
    if state["action"] == "finish":
        return END
    else:
        return "tool"


def build_graph():
    graph = StateGraph(State)
    graph.add_node("agent",agent_node)
    graph.add_node("tool",tool_node)
    graph.add_edge(START,"agent")
    graph.add_conditional_edges(
        "agent",
        route,
        {
            "tool": "tool",
            END: END
        }
    )
    graph.add_edge("tool","agent")
    
    redis_saver = RedisSaver(redis_url = "redis://localhost:6379")
    redis_saver.setup()
    return graph.compile(checkpointer=redis_saver)

    

