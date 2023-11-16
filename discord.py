import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import json
import base64
import os

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

# APP_ID 1174827140546572330
# PUBLIC_KEY 83970e23fd5f02b18bef28bd6dbd81f9618fb740d03a84b53c8621468c248871

# Your existing functions and API key
def encode_image(image_path):
    # ... [your existing function]

api_key = "your_api_key_here"

# Initialize Discord Bot
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot
    if message.author == bot.user:
        return

    # Check if the bot is mentioned
    if bot.user.mentioned_in(message):
        # Process the message to extract image and text
        # This part will need customization based on how the images/text are sent in your server
        image_url, text = extract_image_and_text(message)

        # Encode the image
        base64_image = encode_image(image_url)

        # Prepare payload for OpenAI API
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": text},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": 300
        }

        # Headers for the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # Sending the request to the OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Check response and send back to Discord
        if response.status_code == 200:
            api_response = json.dumps(response.json(), indent=4)
            await message.channel.send(f"Response from GPT-4 Vision API:\n{api_response}")
        else:
            await message.channel.send(f"Failed to get response. Status code: {response.status_code}")

# Replace 'YOUR_DISCORD_TOKEN' with your actual Discord bot token
bot.run('YOUR_DISCORD_TOKEN')
