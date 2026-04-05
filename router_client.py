# router_client.py

import requests
from config import OPENROUTER_API_KEY, OPENROUTER_API_URL, MODEL_PRIORITY

def query_model(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    for model in MODEL_PRIORITY:
        try:
            print(f"Trying model: {model}")
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a classical language expert. Answer clearly and precisely."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }

            response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            content = response.json()["choices"][0]["message"]["content"]
            return content.strip(), model

        except requests.exceptions.RequestException as e:
            print(f"Model {model} failed: {e}")
            continue

    return "All models failed or quota exceeded.", None
