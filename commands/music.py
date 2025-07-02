import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="music", description="Search YouTube by artist and title, and play the top result in a voice channel.")
    @app_commands.describe(artist="Artist name", title="Song title")
    async def music(self, interaction: discord.Interaction, artist: str, title: str):
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("❌ You must be in a voice channel to use this command.", ephemeral=True)
            return

        voice_channel = interaction.user.voice.channel

        if interaction.guild.voice_client is None:
            vc = await voice_channel.connect()
        else:
            vc = interaction.guild.voice_client
            await vc.move_to(voice_channel)

        query = f"{artist} - {title}"
        await interaction.response.send_message(f"🔍 Searching YouTube for **{query}**...", ephemeral=True)

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'noplaylist': True,
                'default_search': 'ytsearch',
                'extract_flat': False
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)['entries'][0]

                video_title = info.get('title', 'Unknown Title')
                uploader = info.get('uploader', 'Unknown Uploader')
                duration = info.get('duration', 0)
                thumbnail = info.get('thumbnail')
                video_url = info.get('webpage_url')
                audio_url = info['url']

            # Convert duration
            mins, secs = divmod(duration, 60)
            hours, mins = divmod(mins, 60)
            duration_str = f"{hours:02}:{mins:02}:{secs:02}" if hours > 0 else f"{mins:02}:{secs:02}"

            # Play audio
            vc.stop()
            vc.play(discord.FFmpegPCMAudio(audio_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))


            # Embed
            embed = discord.Embed(
                title=video_title,
                url=video_url,
                description=f"🎧 Now playing in {voice_channel.mention}",
                color=discord.Color.dark_purple()
            )
            embed.set_thumbnail(url=thumbnail)
            embed.add_field(name="Uploader", value=uploader, inline=True)
            embed.add_field(name="Duration", value=duration_str, inline=True)
            embed.set_footer(text=f"Requested by {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)

            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"[play error] {e}")
            await interaction.followup.send("❌ Could not find or play the requested song.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Music(bot))
