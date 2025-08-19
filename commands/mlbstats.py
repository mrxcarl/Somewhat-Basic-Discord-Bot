import discord
from discord.ext import commands
from discord import app_commands
import statsapi
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import discord

class MLBStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Helper to find today's game IDs for a given team
    def find_game_id(self, team_name: str):
        schedule = statsapi.schedule()
        matches = []
        for game in schedule:
            if team_name.lower() in game['away_name'].lower() or team_name.lower() in game['home_name'].lower():
                matches.append({
                    'game_id': game['game_id'],
                    'away_name': game['away_name'],
                    'home_name': game['home_name'],
                    'status': game['status']
                })
        return matches

    @app_commands.command(name="mlbscore", description="Show today's MLB scores")
    async def mlbscore(self, interaction: "discord.Interaction"):
        games = statsapi.schedule()
        if not games:
            await interaction.response.send_message("No MLB games scheduled today.")
            return

        embed = discord.Embed(title="MLB Scores Today", color=discord.Color.blue())
        for game in games:
            line = f"**{game['away_name']}** {game.get('away_score', 0)} - **{game['home_name']}** {game.get('home_score', 0)}"
            embed.add_field(name=game['status'], value=line, inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mlbbox", description="Show today's box score for a given MLB team")
    async def mlbbox(self, interaction: "discord.Interaction", team_name: str):
        matches = self.find_game_id(team_name)
        if not matches:
            await interaction.response.send_message(f"No game found for team '{team_name}' today.")
            return

        async def send_box(interaction_inner, game_id: int):
            box = statsapi.boxscore(game_id)
            with open("boxscore.txt", "w", encoding="utf-8") as f:
                f.write(box)
            await interaction_inner.response.send_message(file=discord.File("boxscore.txt"))

        # Multiple matches — let the user pick
        if len(matches) > 1:
            embed = discord.Embed(
                title=f"{team_name} Games Today",
                description="Select a game to view box score:",
                color=discord.Color.green()
            )
            view = discord.ui.View()

            for game in matches:
                btn_label = f"{game['away_name']} @ {game['home_name']} - {game['status']}"
                button = discord.ui.Button(label=btn_label, style=discord.ButtonStyle.success)

                async def callback(interaction_inner, gid=game['game_id']):
                    await send_box(interaction_inner, gid)

                button.callback = callback
                view.add_item(button)

            await interaction.response.send_message(embed=embed, view=view)

        else:
            await send_box(interaction, matches[0]['game_id'])


async def setup(bot):
    await bot.add_cog(MLBStats(bot))
