import discord
from discord.ext import commands
from discord import app_commands
import requests
import datetime
from config import IGDB_CLIENT_ID, IGDB_CLIENT_SECRET

class PlayGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.token_info = None  # Cache token info

    def get_igdb_token(self):
        if self.token_info and self.token_info['expires_at'] > datetime.datetime.utcnow():
            return self.token_info['access_token']

        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': IGDB_CLIENT_ID,
            'client_secret': IGDB_CLIENT_SECRET,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, params=params)
        data = response.json()
        access_token = data['access_token']
        expires_in = data['expires_in']
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        self.token_info = {'access_token': access_token, 'expires_at': expires_at}
        return access_token

    def search_game_cover(self, game_name):
        token = self.get_igdb_token()
        headers = {
            'Client-ID': IGDB_CLIENT_ID,
            'Authorization': f'Bearer {token}'
        }
        # Search for the game
        search_url = 'https://api.igdb.com/v4/games'
        search_body = f'search "{game_name}"; fields name,cover; limit 1;'
        search_response = requests.post(search_url, headers=headers, data=search_body)
        search_results = search_response.json()
        if not search_results:
            return None
        game = search_results[0]
        cover_id = game.get('cover')
        if not cover_id:
            return None
        # Get cover image
        cover_url = 'https://api.igdb.com/v4/covers'
        cover_body = f'fields url; where id = {cover_id};'
        cover_response = requests.post(cover_url, headers=headers, data=cover_body)
        cover_results = cover_response.json()
        if not cover_results:
            return None
        cover_url = cover_results[0]['url'].replace('t_thumb', 't_cover_big')
        return f'https:{cover_url}'

    @app_commands.command(name="playgame", description="Announce the game you're about to play.")
    @app_commands.describe(game="Name of the game you're about to play")
    async def playgame(self, interaction: discord.Interaction, game: str):
        await interaction.response.defer(ephemeral=True)

        # Find the #general channel
        general = discord.utils.get(interaction.guild.text_channels, name="general")
        if not general:
            await interaction.followup.send("❌ Couldn't find a #general channel in this server.")
            return

        # Fetch game cover
        cover_url = self.search_game_cover(game)

        # Create embed
        embed = discord.Embed(
            title=f"{interaction.user.display_name} is about to play:",
            description=f"🎮 **{game}**",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        if cover_url:
            embed.set_image(url=cover_url)
        embed.set_footer(text="Let's wish them good luck!")

        # Send to #general
        await general.send(embed=embed)
        await interaction.followup.send("📣 Announced your game in #general!")

async def setup(bot):
    await bot.add_cog(PlayGame(bot))
