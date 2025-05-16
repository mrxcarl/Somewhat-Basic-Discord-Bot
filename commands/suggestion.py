import discord
from discord.ext import commands

class Suggestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = 635252261626445849  # Replace with your Discord user ID

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Suggestion command loaded!")

    @discord.app_commands.command(name="suggest", description="Submit a suggestion to the bot owner.")
    async def suggest(self, interaction: discord.Interaction, suggestion: str):
        await interaction.response.defer(ephemeral=True)

        owner = await self.bot.fetch_user(self.owner_id)
        if owner:
            try:
                embed = discord.Embed(
                    title="📩 New Suggestion",
                    description=suggestion,
                    color=discord.Color.blurple()
                )
                embed.set_footer(text=f"From: {interaction.user} ({interaction.user.id})")
                await owner.send(embed=embed)
                await interaction.followup.send("✅ Your suggestion has been sent! Thank you.", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("❌ Could not send the suggestion to the owner. They might have DMs disabled.", ephemeral=True)
        else:
            await interaction.followup.send("❌ Could not find the owner to send your suggestion.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Suggestion(bot))
