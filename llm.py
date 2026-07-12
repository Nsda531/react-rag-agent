import ollama
import json

def chat(messages):
    response = ollama.chat(
        
        model = "qwen3:4b", 
        messages=messages
    )
    return response["message"]["content"]




