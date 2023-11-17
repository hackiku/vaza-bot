import discord
from discord.ext import commands
from dotenv import load_dotenv
import requests
import base64
import os
import re

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Base prompt for the assistant
base_prompt = ("You are Vaza, a discord bot that helps aerospace engineering students solve CFD problems. Your main goal is to help us ace our tests."
               "When shown class slides or tests, you focus on giving actionable solutions rather than describing what you see. when appropriate, you output matlab code blocks. You answers are always short and actionable. You speak English and Serbian.")

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

async def query_openai(sanitized_message, image_url=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    # Base payload structure
    payload = {
        "model": "gpt-4-vision-preview",
        # "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": []}],
        "max_tokens": 450
    }

    if image_url:
        base64_image = encode_image(image_url)
        payload["messages"][0]["content"].append({"type": "text", "text": base_prompt})
        payload["messages"][0]["content"].append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}})
    else:
        payload["messages"][0]["content"].append({"type": "text", "text": sanitized_message})

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        response_json = response.json()
        content = response_json["choices"][0]["message"]["content"]
        usage = response_json["usage"]
        return content, usage
    else:
        raise Exception(f"OpenAI API error: {response.status_code}, {response.content}")

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        try:
            image_url = message.attachments[0].url if message.attachments else None
            sanitized_message = re.sub(r'<@!?(\d+)>', '', message.content).strip()
            content, usage = await query_openai(sanitized_message, image_url)

            response_message = (
                f"{content}\n"
                f"——\n"
                f"Prompt Tokens: {usage['prompt_tokens']}, "
                f"Completion Tokens: {usage['completion_tokens']}, "
                f"Total Tokens: {usage['total_tokens']}"
            )
            await message.channel.send(response_message)
        except Exception as e:
            await message.channel.send(f"Error: {str(e)}")

bot.run(discord_token)