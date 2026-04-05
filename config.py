# config.py

# === API SETTINGS ===
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# === GOOGLE DOCS INPUT ===
SYNTAX_DOC_URL = "https://docs.google.com/document/d/1Fx81TMaGh_s6vuOqG-6y9WVpVULriO6NrKovcrxqzmA/export?format=txt"
MORPHOLOGY_DOC_URL = "https://docs.google.com/document/d/1pk3CBDM2Vov2tGsfwxIlJp4h2QpPOEYuaqMpBSdBShw/export?format=txt"

# === MODEL PRIORITY ===
# Ordered from best to weakest. Will try top → bottom until one succeeds.
MODEL_PRIORITY = [
    "anthropic/claude-3-haiku",
    "openai/gpt-3.5-turbo",
    "nousresearch/nous-hermes-2-mistral",
    "meta-llama/llama-3-8b-instruct",
    "mistralai/mistral-7b-instruct",
    "gryphe/mythomax-l2-13b"
]
