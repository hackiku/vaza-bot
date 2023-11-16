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

# Initialize Discord Bot
bot = commands.Bot(command_prefix="!")

def encode_image(image_url):
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode('utf-8')

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        # Assuming the image is sent as an attachment
        if message.attachments:
            image_url = message.attachments[0].url
            base64_image = encode_image(image_url)

            # Prepare payload for OpenAI API
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Act as a discord bot. Provide the correct answer to this aerospace uni self-test and explain why in less than 150 words."},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                        ]
                    }
                ],
                "max_tokens": 300
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {openai_api_key}"
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            if response.status_code == 200:
                api_response = json.dumps(response.json(), indent=4)
                await message.channel.send(f"Response from GPT-4 Vision API:\n{api_response}")
            else:
                await message.channel.send(f"Failed to get response. Status code: {response.status_code}")
        else:
            await message.channel.send("No image found in the message.")

bot.run(discord_token)