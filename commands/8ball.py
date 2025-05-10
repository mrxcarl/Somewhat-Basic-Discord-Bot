import discord
from discord.ext import commands
import random

RESPONSES = [
    "Yes! ✅", "No ❌", "Maybe 🤔", "Ask again later ⏳",
    "Definitely! 🎯", "I wouldn't count on it... 😬", "Absolutely! 😃", "Not in a million years! 😵"
]

class Magic8Ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Magic 8-Ball command loaded!")

    @discord.app_commands.command(name="8ball", description="Ask the magic 8-ball a question")
    async def eight_ball(self, interaction: discord.Interaction, question: str):
        response = random.choice(RESPONSES)
        await interaction.response.send_message(f"🎱 **Question:** {question}\n**Answer:** {response}")

async def setup(bot):
    await bot.add_cog(Magic8Ball(bot))
