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
    print(f"✅ Logged in as {bot.user}")
    await bot.tree.sync()  # Sync slash commands with Discord
    print("✅ Slash commands synced!")
    for guild in bot.guilds:
        found_channel = None
        # Option 1: Try to find a channel named 'general'
        for channel in guild.text_channels:
            if channel.name == 'general':
                found_channel = channel
                break
        
        # Option 2: If 'general' isn't found, try the guild's system channel
        # The system channel is often the default "welcome" channel
        if not found_channel and guild.system_channel:
            found_channel = guild.system_channel

        # Option 3: Fallback to the first text channel the bot has permission to send messages to
        if not found_channel:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    found_channel = channel
                    break

        if found_channel:
            try:
                await found_channel.send(f'{bot.user.name} is now online!')
                print(f"Sent online message to {found_channel.name} in {guild.name}")
            except discord.Forbidden:
                print(f"Cannot send message to {found_channel.name} in {guild.name} (Missing permissions)")
            except Exception as e:
                print(f"Error sending message to {found_channel.name} in {guild.name}: {e}")
        else:
            print(f"Could not find a suitable channel to announce in {guild.name}")    

# Run bot
async def main():
    await load_commands()
    await bot.start(TOKEN)

import asyncio
asyncio.run(main())
