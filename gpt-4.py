from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
  
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)

# Define the model
model_name = "gpt-4-1106-preview"

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the basics of aerodynamics in depressing sassy rhymes. 100 words max",
        }
    ],
    model=model_name,
)

# Run the test and print the response
print(chat_completion.message["content"])

