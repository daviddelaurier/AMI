import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key and other configurations from .env file
api_key = os.getenv('GROQ_API_KEY')
input_path = os.getenv('GROQ_TEXT_INPUT')
output_path = os.getenv('GROQ_TEXT_OUTPUT')
system_message = os.getenv('SYSTEM_MESSAGE')

# Initialize the Groq client
client = Groq(api_key=api_key)

# Check if input_path is not None
if input_path is not None:
    # Read the user message from the input file
    with open(input_path, 'r') as file:
        user_message = file.read()
else:
    print("Input path is None, skipping reading from file.")
    user_message = ""

# Send the request to the Groq API
response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
)

# Extract the assistant's response
assistant_response = response.choices[0].message.content

# Write the response to the output file
with open(output_path, 'w') as file:
    file.write(assistant_response)

print(f"Response has been written to {output_path}")