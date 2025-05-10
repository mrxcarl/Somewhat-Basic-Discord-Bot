import discord
from discord.ext import commands

class Stop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Stop command loaded!")

    @discord.app_commands.command(name="stop", description="Stops the music and disconnects the bot from the voice channel.")
    async def stop(self, interaction: discord.Interaction):
        """Stops playback and disconnects the bot from the voice channel."""

        vc = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        # Check if the bot is in a voice channel
        if not vc or not vc.is_connected():
            await interaction.response.send_message("⚠️ I'm not connected to a voice channel!", ephemeral=True)
            return

        # Stop the currently playing audio
        if vc.is_playing():
            vc.stop()

        # Disconnect from the voice channel
        await vc.disconnect()
        await interaction.response.send_message("⏹️ Music stopped, and I have left the voice channel.")

async def setup(bot):
    await bot.add_cog(Stop(bot))
