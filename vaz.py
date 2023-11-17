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

# Define Intents
intents = discord.Intents.default()
intents.messages = True  # Enable the bot to receive messages
intents.message_content = True  # Enable access to message content

# Initialize Discord Bot with Intents
bot = commands.Bot(command_prefix="!", intents=intents)

def encode_image(image_url):
    # Encode the image at the given URL to base64
    response = requests.get(image_url)
    return base64.b64encode(response.content).decode('utf-8')

@bot.event
async def on_ready():
        # listen to bot online/offline events
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    
    # listen to new messages
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        # Process messages with attachments
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
                            {"type": "text", "text": "Act as a discord bot that explains aerospace university class materials. Respond succinctly in 100 words or less"},
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
                response_json=response.json()
                content = response_json["choices"][0]["message"]["content"]
                usage = response_json["usage"]
                
                # prepare response message
                response_message = (
                    f"**Response:**\n{content}\n"
                    f"**Usage:**\n"
                    f"Prompt Tokens: {usage['prompt_tokens']}, "
                    f"Completion Tokens: {usage['completion_tokens']}, "
                    f"Total Tokens: {usage['total_tokens']}"
                )
                await message.channel.send(response_message)
            else:
                error_message = f"Failed to get response. Status code: {response.status_code}\n{response.content.decode()}"
                await message.channel.send(error_message)
            await message.channel.send(error_message)
        else:
            await message.channel.send("No image found in the message.")

bot.run(discord_token)