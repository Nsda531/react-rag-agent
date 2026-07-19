from tools.rag import rag_tool
from tools.calculator import calculator_tool
from tools.weather import weather_tool
from tools.web_search import web_search_tool

TOOLS = {
    "rag": {
        "function": rag_tool,
        "description": "搜索医疗知识库，获取诊疗指南，药品说明和检验指标信息"
    },

    "calculator": {
        "function": calculator_tool,
        "description": "计算数学表达式，例如: 2+3, 13*6"
    },

    "weather": {
        "function": weather_tool,
        "description": "查询天气"
    },

    "web_search": {
        "function": web_search_tool,
        "description": "搜索网页信息，并提炼返回"
    }
}