# question_runner.py

import tempfile
from router_client import query_model
from doc_utils import get_questions_from_doc
from config import SYNTAX_DOC_URL, MORPHOLOGY_DOC_URL

def run_tool(passage, doc_type):
    if not passage.strip():
        return "Please enter a passage to analyze.", None, None
    if not doc_type:
        return "Please select either 'Syntax' or 'Morphology'.", None, None

    try:
        doc_url = SYNTAX_DOC_URL if doc_type.lower() == "syntax" else MORPHOLOGY_DOC_URL
        questions = get_questions_from_doc(doc_url)

        if not questions or questions[0].startswith("Error"):
            return questions[0], None, None

        est_seconds = round(len(questions) * 2.5, 1)
        estimated_time_message = f"Estimated generation time: ~{est_seconds} seconds"

        responses = []
        for idx, question in enumerate(questions):
            prompt = f"""You are a classical language expert.

Given the following Latin or Greek passage:

{passage}

Answer the following question:

{question}

Answer:"""

            raw_response, model_used = query_model(prompt)

            if not raw_response or not model_used:
                formatted_block = f"""Question: {question.strip()}
Answer:
<No answer – all models failed or quota exceeded.>
===
"""
            else:
                answer = raw_response.split("Answer:")[-1].strip()
                formatted_block = f"""Question: {question.strip()}
Answer:
{answer}
Model used: {model_used}
==="""  # Separator for logic tree parsing

            responses.append(formatted_block)

        result = "\n\n".join(responses)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f:
            f.write(result)
            file_path = f.name

        return result, file_path, estimated_time_message

    except Exception as e:
        return f"An error occurred: {str(e)}", None, None
