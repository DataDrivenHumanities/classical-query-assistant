# doc_utils.py

import requests

def get_questions_from_doc(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        questions = [line.strip() for line in text.splitlines() if line.strip().endswith('?')]
        return questions
    except Exception as e:
        return [f"Error loading questions: {e}"]
