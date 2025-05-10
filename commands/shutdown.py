import discord
from discord.ext import commands
import sys
import os

class Shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Shutdown command loaded!")

    @discord.app_commands.command(name="shutdown", description="Shutdown the bot (Admin only)")
    @commands.has_permissions(administrator=True)
    async def shutdown(self, interaction: discord.Interaction):
        """Shutdown the bot."""
        await interaction.response.send_message("🔴 Shutting down the bot... Goodbye!", ephemeral=True)
        
        # Shutting down the bot
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Shutdown(bot))
