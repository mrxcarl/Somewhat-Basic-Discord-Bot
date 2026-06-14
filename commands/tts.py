import discord
from discord.ext import commands
import soundfile as sf
# Import both KokoroPipeline and PipelineConfig from pykokoro
from pykokoro import KokoroPipeline, PipelineConfig
import os
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logging.info("Initializing Kokoro-82M TTS Pipeline...")
        
        # Correct pykokoro syntax: Configuration object must be passed first
        # Defaulting voice to American English ('af_bella')
        self.config = PipelineConfig(voice="am_michael")
        self.pipeline = KokoroPipeline(self.config)
        
        logging.info("Kokoro-82M TTS Pipeline initialized successfully.")

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("✅ TTS command loaded!")
        print("✅ TTS command loaded!")

    @discord.app_commands.command(name="tts", description="Converts text to speech using realistic Kokoro-82M and plays it.")
    async def tts(self, interaction: discord.Interaction, text: str):
        """Plays only the user's text as highly realistic speech in a voice channel."""
        logging.info(f"TTS command invoked by {interaction.user.name} ({interaction.user.id}) with text: '{text}'")

        # Ensure user is in a voice channel
        if not interaction.user.voice or not interaction.user.voice.channel:
            logging.warning(f"User {interaction.user.name} tried to use TTS but was not in a voice channel.")
            await interaction.response.send_message("⚠️ You must be in a voice channel to use this command!", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel
        logging.info(f"User {interaction.user.name} is in voice channel: {voice_channel.name}")

        # Clean text to remove any potential metadata issues
        clean_text = text.strip()
        if not clean_text:
            logging.warning(f"User {interaction.user.name} provided empty text for TTS.")
            await interaction.response.send_message("⚠️ Please provide text to convert to speech!", ephemeral=True)
            return

        # Defer response early because model inference takes a brief moment
        await interaction.response.defer()
        logging.info("Interaction response deferred.")

        # Generate unique file per interaction to prevent concurrency overlap issues
        filename = f"tts_{interaction.id}.wav"
        logging.info(f"Generating Kokoro TTS for cleaned text: '{clean_text}'")
        
        try:
            # Correct pykokoro generation syntax: use pipe.run()
            # It extracts speech samples directly into a single result object
            result = self.pipeline.run(clean_text)
            
            # Extract raw audio array and save via soundfile at Kokoro's native 24kHz rate
            sf.write(filename, result.audio, 24000)
            logging.info(f"Kokoro TTS audio saved to {filename}")
        except Exception as e:
            logging.error(f"Error generating or saving Kokoro TTS file: {e}")
            await interaction.followup.send("❌ An error occurred while generating the speech.", ephemeral=True)
            return

        # Handle voice channel connection/movement
        try:
            vc = discord.utils.get(self.bot.voice_clients, guild=interaction.guild)
            if vc and vc.is_connected():
                logging.info(f"Bot already connected to a voice channel, moving to {voice_channel.name}.")
                await vc.move_to(voice_channel)
            else:
                logging.info(f"Bot not connected, connecting to voice channel: {voice_channel.name}")
                vc = await voice_channel.connect()
        except Exception as e:
            logging.error(f"Error connecting to voice channel: {e}")
            await interaction.followup.send("❌ Could not connect to your voice channel.", ephemeral=True)
            if os.path.exists(filename):
                os.remove(filename)
            return

        # Play the TTS audio
        try:
            vc.play(discord.FFmpegPCMAudio(filename), after=lambda e: logging.info(f"TTS playback finished: {e}" if e else "TTS playback complete."))
            logging.info("Started playing TTS audio.")
        except Exception as e:
            logging.error(f"Error playing TTS audio: {e}")
            await interaction.followup.send("❌ An error occurred while playing the speech.", ephemeral=True)
            
            # Clean up immediately if playback fails to initialize
            if os.path.exists(filename):
                os.remove(filename)
                logging.info(f"Removed '{filename}' due to playback error.")
            if vc.is_connected():
                await vc.disconnect()
                logging.info("Disconnected from voice channel due to playback error.")
            return

        # Wait for playback to finish before deleting the file and disconnecting
        while vc.is_playing():
            await asyncio.sleep(0.5)

        logging.info("TTS playback finished, disconnecting from voice channel.")
        await vc.disconnect()

        # Clean up the generated file safely
        if os.path.exists(filename):
            try:
                os.remove(filename)
                logging.info(f"Removed temporary TTS file: {filename}")
            except Exception as e:
                logging.error(f"Failed to remove file {filename}: {e}")
        else:
            logging.warning(f"Attempted to remove '{filename}', but it did not exist.")

async def setup(bot):
    await bot.add_cog(TTS(bot))
