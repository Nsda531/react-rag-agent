from tools.registry import TOOLS
from resources import RESOURCES

def tool_node(state,resources=None):
    action = state["action"]
    action_input = state["action_input"]
    if action == "finish":
        state["answer"] = action_input
        return state
    #找工具
    tool = TOOLS.get(action)
    if tool is None:
        state["observation"] = f"工具 {action} 不存在"
        return state
    #执行工具   tool["function"]就拿到工具对应的函数
    tool["function"](state,RESOURCES) 
    state["messages"].append({
        "role": "tool",
        "content": str(state["observation"])
    })
    return state