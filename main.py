# main.py

import subprocess
import sys
import webbrowser
import time
import gradio as gr
from question_runner import run_tool
from config import MODEL_PRIORITY, SYNTAX_DOC_URL, MORPHOLOGY_DOC_URL
from doc_utils import get_questions_from_doc

# Auto-install required packages if missing
def install_missing_packages():
    from importlib.metadata import distributions
    required = {"gradio", "requests"}
    installed = {dist.metadata['Name'].lower() for dist in distributions()}
    missing = required - installed

    if missing:
        print(f"Installing missing packages: {missing}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])

install_missing_packages()

# Estimate runtime based on # of questions
def estimate_runtime(passage, doc_type):
    if not passage.strip() or not doc_type:
        return ""
    doc_url = SYNTAX_DOC_URL if doc_type.lower() == "syntax" else MORPHOLOGY_DOC_URL
    questions = get_questions_from_doc(doc_url)
    if not questions or questions[0].startswith("Error"):
        return "Unable to load questions."
    est_seconds = round(len(questions) * 2.5, 1)
    return f"Estimated generation time: ~{est_seconds} seconds"

def launch_app():
    with gr.Blocks(theme="soft") as demo:
        gr.Markdown("""
        ## **Classical Language Query Assistant**
        Submit a Latin or Greek passage and select the question type.
        Answers are generated using a rotating chain of hosted AI models via OpenRouter.

        - Models are attempted in descending priority, starting from the most accurate.
        - The model that answers each question is recorded in the response.
        - Model quota or errors may trigger automatic fallback to the next-best option.
        """)

        with gr.Row():
            passage_input = gr.Textbox(label="Latin or Greek Passage", lines=4)
            question_type = gr.Radio(["Syntax", "Morphology"], label="Question Type")

        top_model = MODEL_PRIORITY[0]
        full_model_list = "\n".join(f"- `{m}`" for m in MODEL_PRIORITY)
        demo_model_info = gr.Markdown(
            f"""
**Currently prioritized model:** `{top_model}`  
**Model fallback chain (if needed):**  
{full_model_list}
""")

        with gr.Row():
            output_text = gr.Textbox(label="Generated Answers", lines=25, interactive=False)
            output_file = gr.File(label="Download Answers (.txt)", interactive=False)

        estimated_time_box = gr.Textbox(label="Estimated Time", interactive=False)

        # Trigger time estimate dynamically
        passage_input.change(fn=estimate_runtime, inputs=[passage_input, question_type], outputs=estimated_time_box)
        question_type.change(fn=estimate_runtime, inputs=[passage_input, question_type], outputs=estimated_time_box)

        submit_button = gr.Button("Generate Answers")

        submit_button.click(
            fn=run_tool,
            inputs=[passage_input, question_type],
            outputs=[output_text, output_file, estimated_time_box]
        )

        # Launch app and open browser
        _, _, share_url = demo.launch(share=True, prevent_thread_lock=True)
        if share_url:
            webbrowser.open(share_url)

        # Keep app running
        while True:
            time.sleep(1)

if __name__ == "__main__":
    launch_app()
