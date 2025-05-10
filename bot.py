import discord
from discord.ext import commands
import os
import importlib

# Load bot token from config.py
from config import TOKEN

# Enable intents
intents = discord.Intents.default()

# Initialize bot with slash commands
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to load commands dynamically
async def load_commands():
    command_dir = "commands"
    
    for filename in os.listdir(command_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{command_dir}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                await bot.load_extension(module_name)
                print(f"Loaded {filename}")
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

# Bot startup event
@bot.event
async def on_ready():
    activity = discord.Game(name="the role of being a bot")  # Change this to your desired status
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ Logged in as {bot.user}")
    await bot.tree.sync()  # Sync slash commands with Discord
    print("✅ Slash commands synced!")

# Run bot
async def main():
    await load_commands()
    await bot.start(TOKEN)

import asyncio
asyncio.run(main())
