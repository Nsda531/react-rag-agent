import requests

def weather_tool(state, resources):
    city = state["action_input"]
    try:
        resp = requests.get(
            f"https://wttr.in/{city}?format=%C+%t+%h+%w",
            timeout = 10 
        )
        state["observation"] = f"{city}天气:{resp.text.strip()}"
    except Exception as e:
        state["observation"] = f"天气查询失败：{e}"
    return state