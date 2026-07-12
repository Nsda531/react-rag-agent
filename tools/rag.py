from retrieval import search

def rag_tool(state,resources):
    context = search(
        state["action_input"],
        resources["model"],
        resources["collection"]
    )
    state["observation"] = context
    return state