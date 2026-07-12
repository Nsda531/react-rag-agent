from typing import TypedDict,List,Any

class State(TypedDict):
    question:str
    chat_history:List[dict]
    messages:list[dict[str,Any]]
    action:str
    action_input:str
    observation:Any
    answer:str