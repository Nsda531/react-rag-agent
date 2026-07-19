from tools.registry import TOOLS
from llm import chat
import json
import re

def safe_json_load(text):
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
            return {"action": "finish" , "action_input": text}
    return json.loads(match.group())

        
REACT_PROMPT = """
你是一个医疗信息助手Agent。
重要提示：你提供的是信息参考，不构成医疗诊断。用户有健康问题应咨询医生。
你可以使用以下工具：
"""
for name,tool in TOOLS.items():
        REACT_PROMPT += f"-{name}:{tool['description']}\n"
REACT_PROMPT += """
你必须严格按照 JSON 格式输出,不允许输出任何多余内容
输出格式如下:
{
    "thought":"你在思考什么",
    "action":"rag | calculator | weather | web_search | finish",
    "action_input":"工具输入或最终答案"
}
规则：
-如果需要工具,就选择 action
-如果可以直接回答用户,就 action = finish
-不要输出 markdown
-不要输出解释
"""

def agent_node(state):
    state.setdefault("messages",[])
    state["action"] = ""
    state["action_input"] = ""
    if not state["messages"]:
        state["messages"] = [
                {"role": "system", "content": REACT_PROMPT},
                {"role": "user", "content": state["question"]}
        ]
    else:
        state["messages"].append({
             "role": "user",
             "content": state["question"]
        })
        state["messages"].append({
             "role": "user",
             "content": "请继续。如果已有足够信息,请用action=finish回答用户"
        })

    response = chat(state["messages"])
    data = safe_json_load(response)
    state["action"] = data["action"]
    state["action_input"] = data["action_input"]
    if state["action"] == "finish":
         disclaimer = "\n\n[注意] 以上信息仅供参考，不构成医疗诊断，如有健康问题请咨询专业医生。"
         state["answer"] = state["action_input"] + disclaimer
    state["messages"].append({
            "role":"assistant",
            "content":response
    })
    return state


    
