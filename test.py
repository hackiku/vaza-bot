import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable the bot to receive messages

# Initialize the bot with intents
bot = commands.Bot(command_prefix="!", intents=intents)

# Event listener for when the bot has switched from offline to online
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

# Event listener for new messages.
@bot.event
async def on_message(message):
    # If the message is from the bot itself, ignore it
    if message.author == bot.user:
        return

    # Respond to mentions
    if bot.user.mentioned_in(message):
        await message.channel.send("Hello! I'm an aerospace bot in training.")

    # Process commands
    await bot.process_commands(message)

# Run the bot with the token
bot.run(discord_token)