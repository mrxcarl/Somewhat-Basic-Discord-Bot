import discord
from discord.ext import commands
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Music command loaded!")

    @discord.app_commands.command(name="music", description="Play any song by any artist from YouTube in a voice channel.")
    async def music(self, interaction: discord.Interaction, song: str, artist: str):
        """Searches YouTube for a song and plays it in a voice channel."""
        
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

        # Search for the song on YouTube
        search_query = f"{song} {artist} official audio"
        await interaction.response.send_message(f"🔍 Searching YouTube for `{song} - {artist}`...")

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{search_query}", download=False)["entries"][0]
                url = info["url"]
                video_title = info["title"]
            except Exception as e:
                await interaction.followup.send(f"❌ Error finding the song: {str(e)}", ephemeral=True)
                return

        # Send a message and play the song
        await interaction.followup.send(f"🎵 Now playing **{video_title}** in {voice_channel.name}!")

        vc.play(discord.FFmpegPCMAudio(url), after=lambda e: print(f"Finished playing: {e}" if e else "Playback finished."))

        # Wait for playback to finish before disconnecting
        while vc.is_playing():
            await asyncio.sleep(1)

        await vc.disconnect()

async def setup(bot):
    await bot.add_cog(Music(bot))
