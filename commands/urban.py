import discord
from discord.ext import commands
import aiohttp

class Urban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Urban Dictionary command loaded!")

    @discord.app_commands.command(name="urban", description="Look up a word on Urban Dictionary.")
    @discord.app_commands.describe(term="The word or phrase to search for")
    async def urban(self, interaction: discord.Interaction, term: str):
        await interaction.response.defer()

        url = f"https://api.urbandictionary.com/v0/define?term={term}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await interaction.followup.send("❌ Failed to reach Urban Dictionary.", ephemeral=True)
                    return

                data = await resp.json()
                if not data["list"]:
                    await interaction.followup.send(f"❌ No results found for **{term}**.", ephemeral=True)
                    return

                result = data["list"][0]
                definition = result["definition"][:1024]
                example = result["example"][:1024]

                embed = discord.Embed(
                    title=f"Urban Dictionary: {term}",
                    url=result["permalink"],
                    color=discord.Color.orange()
                )
                embed.add_field(name="📖 Definition", value=definition, inline=False)
                embed.add_field(name="💬 Example", value=example or "No example provided.", inline=False)
                embed.set_footer(text=f"👍 {result['thumbs_up']} | 👎 {result['thumbs_down']}")

                await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Urban(bot))
