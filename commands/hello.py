import discord
from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Hello command loaded!")

    @discord.app_commands.command(name="hello", description="Replies to you")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Go fuck yourself.")

async def setup(bot):
    await bot.add_cog(Hello(bot))
