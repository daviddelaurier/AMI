# System message


# text_inference.py
#------------------
#System
TEXT_INFERENCE_SYSTEM_MESSAGE = "You are a helpful assistant that can answer questions and help with tasks."

# User
TEXT_INFERENCE_PROMPT = [
    {
        "role": "user",
        "content": "Hello, Claude",
    },
    
]

# image_inference.py
#------------------
#System
IMAGE_INFERENCE_SYSTEM_MESSAGE = "You are a helpful assistant that can answer questions and help with tasks."

IMAGE_INFERENCE_PROMPT = [
    {
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": ""}},
            {"type": "text", "text": "Before providing the answer in <answer> tags, think step by step in <thinking> tags and analyze every part of the image."}
        ]
    },
]

# rag.py
#------------------
#System
RAG_SYSTEM_MESSAGE = "You are a helpful assistant that can answer questions and help with tasks."

# User
RAG_PROMPT = [
    
]