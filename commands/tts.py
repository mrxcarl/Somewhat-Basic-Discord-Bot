import discord
from discord.ext import commands
from gtts import gTTS
import os
import asyncio

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ TTS command loaded!")

    @discord.app_commands.command(name="tts", description="Converts text to speech and plays it in a voice channel.")
    async def tts(self, interaction: discord.Interaction, text: str):
        """Plays only the user's text as speech in a voice channel."""
        
        # Ensure user is in a voice channel
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

        # Clean text to remove any potential metadata issues
        clean_text = text.strip()  # Ensures no leading/trailing spaces
        if not clean_text:
            await interaction.response.send_message("⚠️ Please provide text to convert to speech!", ephemeral=True)
            return

        # Generate speech file
        tts = gTTS(text=clean_text, lang="en")
        filename = "tts_output.mp3"
        tts.save(filename)

        # Defer response to prevent auto-responses interfering with TTS
        await interaction.response.defer()

        # Play the TTS audio
        vc.play(discord.FFmpegPCMAudio(filename), after=lambda e: print(f"TTS playback finished: {e}" if e else "TTS playback complete."))

        # Wait for playback to finish before deleting the file and disconnecting
        while vc.is_playing():
            await asyncio.sleep(1)

        await vc.disconnect()

        # Clean up the generated file
        os.remove(filename)

async def setup(bot):
    await bot.add_cog(TTS(bot))
