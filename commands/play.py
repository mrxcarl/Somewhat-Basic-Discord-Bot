import discord
from discord.ext import commands
import asyncio

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Play command loaded!")

    @discord.app_commands.command(name="play", description="Play a local MP3 file in a voice channel.")
    async def play(self, interaction: discord.Interaction):
        """Joins the user's voice channel and plays a local MP3 file."""

        # Check if user is in a voice channel
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("⚠️ You must be in a voice channel to use this command!", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel
        vc = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        # If already connected, move to the user's channel
        if vc and vc.is_connected():
            await vc.move_to(voice_channel)
        else:
            vc = await voice_channel.connect()

        # Define the path to your MP3 file (update this!)
        mp3_file = "audio/mp3.mp3"

        # Check if the bot is already playing audio
        if vc.is_playing():
            await interaction.response.send_message("⚠️ I'm already playing audio!", ephemeral=True)
            return

        # Send a response message
        await interaction.response.send_message(f"🎵 Playing `{mp3_file}` in {voice_channel.name}!")

        # Play the audio file
        vc.play(discord.FFmpegPCMAudio(mp3_file), after=lambda e: print(f"Finished playing: {e}" if e else "Playback finished."))

        # Wait for playback to finish before disconnecting
        while vc.is_playing():
            await asyncio.sleep(1)

        await vc.disconnect()

async def setup(bot):
    await bot.add_cog(Play(bot))
