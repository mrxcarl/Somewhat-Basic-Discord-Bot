import discord
from discord.ext import commands
import os
import importlib
import asyncio
import random
import datetime
# Load bot token and other configs from config.py
from config import TOKEN, CHANNEL_ID

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
    await bot.tree.sync()
    print("✅ Slash commands synced!")

    # --- Startup Message Logic ---
    # Now pulling from config.py instead of being hardcoded
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        try:
            with open("startup.txt", "r", encoding="utf-8") as f:
                announcements = [line.strip() for line in f.readlines() if line.strip()]
            
            message_text = random.choice(announcements) if announcements else "Have No Fear, Odahviing is here!"
            
            # Create the Embed
            embed = discord.Embed(
                title="✨ System Online",
                description=f"**{message_text}**",
                color=discord.Color.purple()
            )
            embed.add_field(name="Status", value="🟢 Online", inline=True)
            embed.add_field(name="Host", value="Odahviing", inline=True)
            embed.set_footer(text="System Reboot Complete")
            embed.timestamp = datetime.datetime.now()

            # Send the embed
            sent_msg = await channel.send(embed=embed)
            print(f"✅ Sent embed message to channel {CHANNEL_ID}")

            # Wait 30 seconds and delete
            await asyncio.sleep(30)
            await sent_msg.delete()
            print(f"🗑️ Deleted startup message from channel {CHANNEL_ID}")

        except FileNotFoundError:
            print("⚠️ startup.txt not found! Falling back to default embed.")
            embed = discord.Embed(title="System Online", description="Have No Fear, Odahviing is here!", color=discord.Color.blue())
            sent_msg = await channel.send(embed=embed)
            await asyncio.sleep(30)
            await sent_msg.delete()
    else:
        print(f"⚠️ Could not find channel {CHANNEL_ID}")
    # ------------------------------

# Run bot
async def main():
    await load_commands()
    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())