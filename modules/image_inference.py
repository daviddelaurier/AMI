import os
import base64
from anthropic import Anthropic
from dotenv import load_dotenv
from prompts import IMAGE_INFERENCE_SYSTEM_MESSAGE, IMAGE_INFERENCE_PROMPT

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL_NAME = "claude-3-opus-20240229"

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode('utf-8')
        return base64_string

def main():
    image_data = get_base64_encoded_image("../images/best_practices/nine_dogs.jpg")
    
    messages = IMAGE_INFERENCE_PROMPT.copy()
    messages[0]["content"][0]["source"]["data"] = image_data

    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2048,
        system=IMAGE_INFERENCE_SYSTEM_MESSAGE,
        messages=messages
    )
    print(response.content[0].text)

if __name__ == "__main__":
    main()