import os
import json
import requests

AI_PROXY_URL = "http://127.0.0.1:8082/v1/chat/completions" 
API_KEY = os.getenv("AIPROXY_TOKEN")


URL_CHAT = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
URL_EMBEDDING = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"

def call_llm(prompt: str, schema1: dict):
    headers = {
        "Authorization": f"Bearer {API_KEY}",  # Ensure API_KEY is set
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "response_format": {
            "type": "json_schema",
            "json_schema": schema1
        },

        "temperature":1,
        "max_completion_tokens":2048,
        "top_p":1,
        "frequency_penalty":0,
        "presence_penalty":0
    }
    response = requests.post(AI_PROXY_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        print(f"❌ ERROR: {response.status_code} - {response.text}")
        return None


# Example usage:
if __name__ == "__main__":
    prompt = "Write the first line of the 10 most recent .log file in /data/logs/ to /data/logs-recent.txt, most recent first"
    with open('schema.json', 'r') as file:
        schema = json.load(file)
    result = call_llm(prompt, schema["task_schema"]["A5."])
    print(result)