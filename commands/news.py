import discord
from discord.ext import commands
from discord import app_commands
import requests
from config import NEWS_API_KEY  # Store your API key in config.py

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="news", description="Get the latest news headlines.")
    @app_commands.describe(query="Topic to search for (optional)")
    async def news(self, interaction: discord.Interaction, query: str = None):
        await interaction.response.defer()

        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "country": "us",
            "pageSize": 5
        }

        if query:
            url = "https://newsapi.org/v2/everything"
            params = {
                "apiKey": NEWS_API_KEY,
                "q": query,
                "sortBy": "publishedAt",
                "language": "en",
                "pageSize": 5
            }

        try:
            response = requests.get(url, params=params)
            data = response.json()

            if data.get("status") != "ok" or not data.get("articles"):
                await interaction.followup.send("❌ Couldn't find any news articles.")
                return

            embed = discord.Embed(
                title="📰 Latest News Headlines" if not query else f"📰 News on '{query}'",
                color=discord.Color.blurple()
            )

            for article in data["articles"]:
                title = article["title"][:256]
                url = article["url"]
                embed.add_field(name=title, value=f"[Read more]({url})", inline=False)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"[news error] {e}")
            await interaction.followup.send("❌ Failed to fetch news.")

async def setup(bot):
    await bot.add_cog(News(bot))
