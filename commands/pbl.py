import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp

class PlayByLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pbl", description="Play a YouTube video in a voice channel by link.")
    @app_commands.describe(link="Direct YouTube link")
    async def pbl(self, interaction: discord.Interaction, link: str):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("❌ You must be in a voice channel to use this command.", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel

        if interaction.guild.voice_client is None:
            vc = await voice_channel.connect()
        else:
            vc = interaction.guild.voice_client
            await vc.move_to(voice_channel)

        await interaction.response.send_message("🔗 Fetching YouTube video...", ephemeral=True)

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'noplaylist': True,
                'extract_flat': False
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)

                title = info.get('title', 'Unknown Title')
                uploader = info.get('uploader', 'Unknown Uploader')
                duration = info.get('duration', 0)
                thumbnail = info.get('thumbnail')
                webpage_url = info.get('webpage_url')
                audio_url = info['url']

            # Format duration
            mins, secs = divmod(duration, 60)
            hours, mins = divmod(mins, 60)
            duration_str = f"{hours:02}:{mins:02}:{secs:02}" if hours > 0 else f"{mins:02}:{secs:02}"

            # Play audio
            vc.stop()
            vc.play(discord.FFmpegPCMAudio(audio_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))

            # Embed
            embed = discord.Embed(
                title=title,
                url=webpage_url,
                description=f"🎶 Now playing in {voice_channel.mention}",
                color=discord.Color.blurple()
            )
            embed.set_thumbnail(url=thumbnail)
            embed.add_field(name="Uploader", value=uploader, inline=True)
            embed.add_field(name="Duration", value=duration_str, inline=True)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"[pbl error] {e}")
            await interaction.followup.send("❌ Could not play the audio. Please check the link.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PlayByLink(bot))
