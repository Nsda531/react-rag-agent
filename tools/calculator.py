def calculator_tool(state,resources):
    expression = state["action_input"]
    result = eval(expression)
    state["observation"] = result
    return state
    