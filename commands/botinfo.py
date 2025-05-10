import discord
from discord.ext import commands
import datetime
import platform
import psutil

class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.launch_time = datetime.datetime.utcnow()

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ BotInfo command loaded!")

    @discord.app_commands.command(name="botinfo", description="Displays information about the bot.")
    async def botinfo(self, interaction: discord.Interaction):
        uptime = datetime.datetime.utcnow() - self.launch_time
        uptime_str = str(uptime).split('.')[0]  # Remove microseconds

        embed = discord.Embed(title="🤖 Bot Info", color=discord.Color.green())
        embed.add_field(name="👤 Developer", value="Erendreich", inline=True)
        embed.add_field(name="📡 Servers", value=f"{len(self.bot.guilds)}", inline=True)
        embed.add_field(name="👥 Users", value=f"{len(set(self.bot.users))}", inline=True)
        embed.add_field(name="🕒 Uptime", value=uptime_str, inline=True)
        embed.add_field(name="⚙️ Python", value=platform.python_version(), inline=True)
        embed.add_field(name="🔧 Discord.py", value=discord.__version__, inline=True)
        embed.add_field(name="📊 Memory Usage", value=f"{psutil.Process().memory_info().rss / 1024 / 1024:.2f} MB", inline=True)
        embed.set_footer(text=f"Ping: {round(self.bot.latency * 1000)} ms")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(BotInfo(bot))
