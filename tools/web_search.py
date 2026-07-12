from duckduckgo_search import DDGS

def web_search_tool(state, resources):
    query = state["action_input"]
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        if not results:
            state["observation"] = "未搜到结果"
        else:
            lines = []
            for r in results:
                lines.append(f"-{r['title']}:{r['body']}")
            state["observation"] = "\n".join(lines)
    except Exception as e:
        state["observation"] = f"网页搜索失败：{e}"
    return state
            