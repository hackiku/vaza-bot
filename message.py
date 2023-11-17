import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Retrieve the Discord token from the environment variable
discord_token = os.getenv("DISCORD_TOKEN")

# Check if the Discord token is available
if not discord_token:
    raise ValueError("No Discord token found in environment variables.")

# Define Intents (optional: specify particular intents based on your requirement)
intents = discord.Intents.default()
intents.messages = True  # Enable the bot to receive messages

# Initialize Discord Bot with Intents
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Sanitize the message to remove user mentions
    sanitized_message = re.sub(r'<@!?(\d+)>', '', message.content).strip()

    # Print the sanitized message content to the CLI
    print(f"{sanitized_message}")

# Run the bot with the token
bot.run(discord_token)
