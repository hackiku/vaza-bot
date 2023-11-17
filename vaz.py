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

# Base prompt for the assistant
base_prompt = ("Your name is Vaza, the all-knowing smartass AI companion to a bunch of aerospace engineering students. Always say your name in your responses introducing yourself."
               "You know all about CFD, aerodynamics, rocket science, aviation and are hell-bent of helping us ace our classes in any way possible. You keep answers lively, engaging, youthful, and short"
               )

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
    # Inform when the bot is connected
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    # Check if the message author is the bot itself
    if message.author == bot.user:
        return
    
    # Check if the bot is mentioned in the message
    if bot.user.mentioned_in(message):
        user_message = message.content

        # Define a base payload structure for the API call
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": []
                }
            ],
            "max_tokens": 500
        }

        # If there's an attachment, it's an image for the vision model
        if message.attachments:
            image_url = message.attachments[0].url
            base64_image = encode_image(image_url)

            # Add the image and text to the payload
            payload["messages"][0]["content"].append({"type": "text", "text": base_prompt})
            payload["messages"][0]["content"].append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "auto"}})
        else:
            # If no image is present, just add the text to the payload
            payload["messages"][0]["content"].append({"type": "text", "text": user_message})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        # Send the request to the OpenAI API
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Handle the response from the API
        if response.status_code == 200:
            response_json = response.json()
            content = response_json["choices"][0]["message"]["content"]
            usage = response_json["usage"]
            
            # Prepare the response message for Discord
            response_message = (
                f"**Response:**\n{content}\n"
                f"——\n"
                f"prompt tokens: {usage['prompt_tokens']}, "
                f"completion tokens: {usage['completion_tokens']}, "
                f"total tokens: {usage['total_tokens']}"
            )
            await message.channel.send(response_message)
        else:
            error_message = f"Failed to get response. Status code: {response.status_code}\n{response.content.decode()}"
            await message.channel.send(error_message)

bot.run(discord_token)