import requests
from dotenv import load_dotenv
import os
import base64

# Load environment variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Base prompt for the assistant
base_prompt = ("You are Vaza, a discord bot that helps aerospace engineering students solve CFD problems. Your main goal is to help us ace our tests."
               "When shown class slides or tests, you focus on giving actionable solutions rather than describing what you see. Your answers are always short and actionable. You speak English and Serbian.")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def query_openai(user_message, image_path=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    # Base payload structure
    payload = {
        "model": "gpt-4-vision-preview",  # or "gpt-3.5-turbo" based on your preference
        "messages": [{"role": "user", "content": base_prompt}]
    }

    # If an image is provided, add it to the payload
    if image_path:
        base64_image = encode_image(image_path)
        payload["messages"].append({"role": "user", "content": {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}})

    # Add the text message
    payload["messages"].append({"role": "user", "content": user_message})

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"]
        return content
    else:
        raise Exception(f"OpenAI API error: {response.status_code}, {response.content}")

# Test user message and image
test_message = "Explain what is shown in this image related to aerodynamics. And introduce yourself by name."
image_path = "./image.jpg"

# Run the query and print the response
try:
    response_content = query_openai(test_message, image_path)
    print(response_content)
except Exception as e:
    print(f"Error: {str(e)}")
