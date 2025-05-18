import discord
from discord.ext import commands

class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ GitHub command loaded!")

    @discord.app_commands.command(name="github", description="View the bot's GitHub repository.")
    async def github(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="💻 GitHub Repository",
            description="[Click here to view the source code on GitHub](https://github.com/mrxcarl/Somewhat-Basic-Discord-Bot.git)",
            color=discord.Color.dark_gray()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(GitHub(bot))
