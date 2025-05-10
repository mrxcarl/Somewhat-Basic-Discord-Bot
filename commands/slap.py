import discord
from discord.ext import commands

class Slap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Slap command loaded!")

    @discord.app_commands.command(name="slap", description="Slap a user with a rotting trout!")
    async def slap(self, interaction: discord.Interaction, user: discord.Member):
        """Sends a fun slap message and a private DM to the slapped user."""
        if user == interaction.user:
            await interaction.response.send_message("😆 You can't slap yourself!", ephemeral=True)
            return

        # Public message in the channel
        message = f"💥 {interaction.user.mention} slaps {user.mention} with a rotting trout! 🐟"
        await interaction.response.send_message(message)

        # Private message to the slapped user
        try:
            await user.send(f"💀 You just got slapped with a rotting trout by {interaction.user.display_name}! 🐟")
        except discord.Forbidden:
            await interaction.followup.send(f"❌ Couldn't DM {user.display_name}, they might have DMs disabled.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Slap(bot))
