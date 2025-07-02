import discord
from discord.ext import commands
from gtts import gTTS
import os
import asyncio
import logging # Import the logging module

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("✅ TTS command loaded!") # Use logging.info
        print("✅ TTS command loaded!") # Keep print for immediate console feedback if desired

    @discord.app_commands.command(name="tts", description="Converts text to speech and plays it in a voice channel.")
    async def tts(self, interaction: discord.Interaction, text: str):
        """Plays only the user's text as speech in a voice channel."""
        
        logging.info(f"TTS command invoked by {interaction.user.name} ({interaction.user.id}) with text: '{text}'")

        # Ensure user is in a voice channel
        if not interaction.user.voice or not interaction.user.voice.channel:
            logging.warning(f"User {interaction.user.name} tried to use TTS but was not in a voice channel.")
            await interaction.response.send_message("⚠️ You must be in a voice channel to use this command!", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel
        logging.info(f"User {interaction.user.name} is in voice channel: {voice_channel.name}")
        vc = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)

        # If already connected, move to the user's channel
        if vc and vc.is_connected():
            logging.info(f"Bot already connected to a voice channel, moving to {voice_channel.name}.")
            await vc.move_to(voice_channel)
        else:
            logging.info(f"Bot not connected, connecting to voice channel: {voice_channel.name}")
            vc = await voice_channel.connect()

        # Clean text to remove any potential metadata issues
        clean_text = text.strip()  # Ensures no leading/trailing spaces
        if not clean_text:
            logging.warning(f"User {interaction.user.name} provided empty text for TTS.")
            await interaction.response.send_message("⚠️ Please provide text to convert to speech!", ephemeral=True)
            return

        logging.info(f"Generating TTS for cleaned text: '{clean_text}'")
        # Generate speech file
        try:
            tts = gTTS(text=clean_text, lang="en", tld="us")
            filename = "tts_output.mp3"
            tts.save(filename)
            logging.info(f"TTS audio saved to {filename}")
        except Exception as e:
            logging.error(f"Error generating or saving TTS file: {e}")
            await interaction.response.send_message("❌ An error occurred while generating the speech.", ephemeral=True)
            return

        # Defer response to prevent auto-responses interfering with TTS
        await interaction.response.defer()
        logging.info("Interaction response deferred.")

        # Play the TTS audio
        try:
            vc.play(discord.FFmpegPCMAudio(filename), after=lambda e: logging.info(f"TTS playback finished: {e}" if e else "TTS playback complete."))
            logging.info("Started playing TTS audio.")
        except Exception as e:
            logging.error(f"Error playing TTS audio: {e}")
            await interaction.followup.send("❌ An error occurred while playing the speech.", ephemeral=True)
            # Clean up in case of playback error before waiting
            if os.path.exists(filename):
                os.remove(filename)
                logging.info(f"Removed '{filename}' due to playback error.")
            if vc.is_connected():
                await vc.disconnect()
                logging.info("Disconnected from voice channel due to playback error.")
            return

        # Wait for playback to finish before deleting the file and disconnecting
        while vc.is_playing():
            await asyncio.sleep(1)
        logging.info("TTS playback finished, disconnecting from voice channel.")

        await vc.disconnect()

        # Clean up the generated file
        if os.path.exists(filename):
            os.remove(filename)
            logging.info(f"Removed temporary TTS file: {filename}")
        else:
            logging.warning(f"Attempted to remove '{filename}', but it did not exist.")


async def setup(bot):
    await bot.add_cog(TTS(bot))