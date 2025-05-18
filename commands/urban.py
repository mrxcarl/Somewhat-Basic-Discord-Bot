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
                definitions = data["list"]
                if not definitions:
                    await interaction.followup.send(f"❌ No results found for **{term}**.", ephemeral=True)
                    return

                # Create the view and send the first definition
                view = UrbanPaginator(definitions)
                embed = view.create_embed(0)
                await interaction.followup.send(embed=embed, view=view, ephemeral=False)

class UrbanPaginator(discord.ui.View):
    def __init__(self, definitions):
        super().__init__(timeout=60)
        self.definitions = definitions
        self.index = 0

    def create_embed(self, index):
        entry = self.definitions[index]
        definition = entry["definition"][:1024]
        example = entry["example"][:1024] if entry["example"] else "No example provided."

        embed = discord.Embed(
            title=f"Urban Dictionary: {entry['word']}",
            url=entry["permalink"],
            color=discord.Color.orange()
        )
        embed.add_field(name="📖 Definition", value=definition, inline=False)
        embed.add_field(name="💬 Example", value=example, inline=False)
        embed.set_footer(text=f"👍 {entry['thumbs_up']} | 👎 {entry['thumbs_down']} • Page {self.index + 1} of {len(self.definitions)}")
        return embed

    @discord.ui.button(label="⬅ Previous", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index > 0:
            self.index -= 1
            await interaction.response.edit_message(embed=self.create_embed(self.index), view=self)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Next ➡", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.index < len(self.definitions) - 1:
            self.index += 1
            await interaction.response.edit_message(embed=self.create_embed(self.index), view=self)
        else:
            await interaction.response.defer()

async def setup(bot):
    await bot.add_cog(Urban(bot))
