import base64
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
MODEL_NAME = "claude-3-opus-20240229"

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()
        base_64_encoded_data = base64.b64encode(binary_data)
        base64_string = base_64_encoded_data.decode('utf-8')
        return base64_string


message_list = [
    {
        "role": 'user',
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": get_base64_encoded_image("../images/best_practices/nine_dogs.jpg")}},
            {"type": "text", "text": "You have perfect vision and pay great attention to detail which makes you an expert describing the image and all of its details. Before providing the answer in <answer> tags, think step by step in <thinking> tags and analyze every part of the image."}
        ]
    },
    {
        "role": 'assistant',
        "content": [
            {"type": "text", "text": "I will think step by step in <thinking> tags and analyze every part of the image. Then I will provide the answer in <answer> tags."}
        ]
    }
]

response = client.messages.create(
    model=MODEL_NAME,
    max_tokens=2048,
    messages=message_list
)
print(response.content[0].text)