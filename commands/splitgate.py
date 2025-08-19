import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO

STATS_FILE = "splitgate_stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

class SplitgateStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="sgadd", description="Add your Splitgate match result.")
    @app_commands.describe(kills="Your kills", deaths="Your deaths", won="Did your team win?")
    async def sgadd(self, interaction: discord.Interaction, kills: int, deaths: int, won: bool):
        stats = load_stats()
        uid = str(interaction.user.id)
        timestamp = datetime.utcnow().isoformat()

        if uid not in stats:
            stats[uid] = {
                "games": [],
                "total_kills": 0,
                "total_deaths": 0,
                "wins": 0,
                "losses": 0
            }

        stats[uid]["games"].append({
            "timestamp": timestamp,
            "kills": kills,
            "deaths": deaths,
            "result": "win" if won else "loss"
        })
        stats[uid]["total_kills"] += kills
        stats[uid]["total_deaths"] += deaths
        if won:
            stats[uid]["wins"] += 1
        else:
            stats[uid]["losses"] += 1

        save_stats(stats)

        # Calculate K/D ratio for this match
        kd_ratio = kills / deaths if deaths > 0 else float('inf')
        kd_display = f"{kd_ratio:.2f}" if deaths > 0 else "∞"

        # Create announcement embed
        embed = discord.Embed(
            title=f"🎮 New Splitgate Match Result for {interaction.user.display_name}",
            color=discord.Color.green() if won else discord.Color.red()
        )
        embed.add_field(name="Kills", value=str(kills), inline=True)
        embed.add_field(name="Deaths", value=str(deaths), inline=True)
        embed.add_field(name="K/D Ratio", value=kd_display, inline=True)
        embed.add_field(name="Result", value="Win" if won else "Loss", inline=True)
        embed.set_footer(text=f"Match recorded at {timestamp[:10]}")

        # Send announcement to the channel
        await interaction.channel.send(embed=embed)
        # Send confirmation to the user
        await interaction.response.send_message("✅ Your match stats have been saved.", ephemeral=True)

    @app_commands.command(name="sgstats", description="Show Splitgate stats for a user.")
    @app_commands.describe(user="The user to view stats for")
    async def sgstats(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        stats = load_stats()
        data = stats.get(str(user.id))

        if not data:
            await interaction.response.send_message("❌ No stats found for that user.")
            return

        total_kills = data["total_kills"]
        total_deaths = data["total_deaths"]
        kd_ratio = total_kills / total_deaths if total_deaths > 0 else float('inf')

        embed = discord.Embed(title=f"📊 Splitgate Stats for {user.display_name}", color=discord.Color.orange())
        embed.add_field(name="Total Games", value=str(len(data["games"])), inline=True)
        embed.add_field(name="Total Kills", value=str(total_kills), inline=True)
        embed.add_field(name="Total Deaths", value=str(total_deaths), inline=True)
        embed.add_field(name="K/D Ratio", value=f"{kd_ratio:.2f}", inline=True)
        embed.add_field(name="Wins", value=str(data["wins"]), inline=True)
        embed.add_field(name="Losses", value=str(data["losses"]), inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sghistory", description="Show the last few Splitgate matches for a user.")
    @app_commands.describe(user="The user to view match history for")
    async def sghistory(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        stats = load_stats()
        data = stats.get(str(user.id))

        if not data or not data.get("games"):
            await interaction.response.send_message("❌ No match history found for that user.")
            return

        games = data["games"][-10:]  # Last 10 matches
        embed = discord.Embed(title=f"🕹️ Last 10 Splitgate Matches for {user.display_name}", color=discord.Color.teal())
        for i, game in enumerate(games, 1):
            embed.add_field(
                name=f"Game {i} - {game['timestamp'][:10]}",
                value=f"Kills: {game['kills']}, Deaths: {game['deaths']}, Result: {game['result'].capitalize()}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sggraph", description="Show a kill/death trend graph for a user.")
    @app_commands.describe(user="The user to generate a graph for")
    async def sggraph(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        stats = load_stats()
        data = stats.get(str(user.id))

        if not data or not data.get("games"):
            await interaction.response.send_message("❌ No data available to generate a graph.")
            return

        games = data["games"]
        kill_list = [g["kills"] for g in games]
        death_list = [g["deaths"] for g in games]
        match_nums = list(range(1, len(games) + 1))

        plt.figure(figsize=(10, 5))
        plt.plot(match_nums, kill_list, label="Kills", marker='o')
        plt.plot(match_nums, death_list, label="Deaths", marker='x')
        plt.xlabel("Match Number")
        plt.ylabel("Count")
        plt.title(f"Splitgate Performance - {user.display_name}")
        plt.legend()
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        file = discord.File(fp=buffer, filename="splitgate_stats.png")

        await interaction.response.send_message(file=file)
        buffer.close()
        plt.close()

async def setup(bot):
    await bot.add_cog(SplitgateStats(bot))