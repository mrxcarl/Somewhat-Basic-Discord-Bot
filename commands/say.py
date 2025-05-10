import discord
from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Say command loaded!")

    @discord.app_commands.command(name="say", description="Make the bot say whatever you want.")
    async def say(self, interaction: discord.Interaction, message: str):
        """Repeats the user's message."""
        await interaction.response.send_message(message)

async def setup(bot):
    await bot.add_cog(Say(bot))
