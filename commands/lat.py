import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import time

class LatencyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="lat", description="Check bot latency and Ubisoft server latency")
    async def lat(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)

        # Bot WebSocket latency
        ws_latency = round(self.bot.latency * 1000, 2)

        # Optional: HTTP ping to Ubisoft's public API gateway (safe)
        ubisoft_url = "https://public-ubiservices.ubi.com/v1/profiles"
        try:
            start = time.perf_counter()
            async with aiohttp.ClientSession() as session:
                async with session.get(ubisoft_url, timeout=5) as resp:
                    end = time.perf_counter()
                    http_latency = round((end - start) * 1000, 2)
                    status = resp.status
        except Exception as e:
            http_latency = None
            status = f"Error: {e}"

        embed = discord.Embed(
            title="🏓 Latency Check",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Bot Latency", value=f"{ws_latency} ms")
        if http_latency:
            embed.add_field(name="Ubisoft API", value=f"{http_latency} ms (Status {status})")
        else:
            embed.add_field(name="Ubisoft API", value=f"❌ {status}")

        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(LatencyCog(bot))
