import requests
from config import OLLAMA_API_URL,OLLAMA_MODEL,OLLAMA_TEMPERATURE

def chat(messages):
    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False,
            "options":{"temperature": OLLAMA_TEMPERATURE}
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"]




