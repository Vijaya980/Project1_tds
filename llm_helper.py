import os
import requests
import json
import re
from typing import Optional, Tuple


URL_CHAT = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
URL_EMBEDDING = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"

# Check for API key in environment variables
api_key = os.getenv("AIPROXY_TOKEN") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Set AIPROXY_TOKEN or OPENAI_API_KEY.")

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


def parse_llm_output(llm_response: str) -> Tuple[Optional[dict], Optional[str]]:
    """
    Parses LLM output and extracts JSON or Python code.

    Args:
        llm_response (str): The output string from LLM.

    Returns:
        Tuple[Optional[dict], Optional[str]]: Parsed JSON object (if present) and extracted Python code (if present).
    """
    json_pattern = re.search(r'```json\n(.*?)\n```', llm_response, re.DOTALL)
    python_pattern = re.search(r'```python\n(.*?)\n```', llm_response, re.DOTALL)
    json_data = None
    python_code = None
    if json_pattern:
        try:
            json_data = json.loads(json_pattern.group(1))
        except json.JSONDecodeError:
            pass  # Ignore JSON parsing errors
    if python_pattern:
        python_code = python_pattern.group(1)
    return json_data, python_code

def call_llm_prompt(prompt: str, system_message: Optional[str] = None) -> str:
    """Calls AI Proxy for chat completion."""
    messages = [{"role": "user", "content": prompt}]
    if system_message:
        messages.insert(0, {"role": "system", "content": system_message})
    payload = {
        "model": "gpt-4o-mini",
        "messages": messages
    }

    response = requests.post(URL_CHAT, headers=HEADERS, json=payload)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]

def get_embedding(text: str) -> list:
    """Calls AI Proxy for text embeddings."""
    payload = {
        "model": "text-embedding-3-small",
        "input": text
    }
    response = requests.post(URL_EMBEDDING, headers=HEADERS, json=payload)
    response.raise_for_status()
    result = response.json()
    return result["data"][0]["embedding"]
def call_llm(prompt: str, schema1: json) -> json:
    payload = {
        "model":"gpt-4o-mini",
        "messages":[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
                },
            ]
            }
        ],
        "response_format":{
                "type": "json_schema",
                "json_schema": schema1
        },
        "temperature":1,
        "max_completion_tokens":2048,
        "top_p":1,
        "frequency_penalty":0,
        "presence_penalty":0
    }

    response = requests.post(URL_CHAT, headers=HEADERS, json=payload)
    response.raise_for_status()
    result = response.json()
    return json.loads(result["choices"][0]["message"]["content"])


# Example usage:
if __name__ == "__main__":
    prompt = "Generate a JSON object with a user's name, age, and email."
    result = call_llm_prompt(prompt)
    print(result)

    prompt = "Write the first line of the 10 most recent .log file in /data/logs/ to /data/logs-recent.txt, most recent first"
    with open('schema.json', 'r') as file:
        schema = json.load(file)
    result = call_llm(prompt, schema["task_schema"]["A5."])
    print(result)