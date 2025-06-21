import discord
from discord.ext import commands
from discord import app_commands
import json
import os

BETS_FILE = "data/betslips.json"

# Ensure the data directory exists
os.makedirs(os.path.dirname(BETS_FILE), exist_ok=True)

def load_bets():
    if not os.path.exists(BETS_FILE):
        return {}
    with open(BETS_FILE, "r") as f:
        return json.load(f)

def save_bets(data):
    with open(BETS_FILE, "w") as f:
        json.dump(data, f, indent=4)

class SportsBetting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_user_bets(self, user_id: str):
        data = load_bets()
        return data.get(user_id, [])

    def update_user_bets(self, user_id: str, bets):
        data = load_bets()
        data[user_id] = bets
        save_bets(data)

    @app_commands.command(name="add", description="Add a bet to your betslip.")
    @app_commands.describe(bet="Describe your bet", odds="The odds (e.g., +150 or -110)")
    async def add(self, interaction: discord.Interaction, bet: str, odds: str):
        user_id = str(interaction.user.id)
        bets = self.get_user_bets(user_id)
        bets.append({"bet": bet, "odds": odds, "status": "open"})
        self.update_user_bets(user_id, bets)
        await interaction.response.send_message(f"✅ Bet added: **{bet}** at **{odds}**", ephemeral=True)

    @app_commands.command(name="clearslip", description="Clear your entire betslip.")
    async def clearslip(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        self.update_user_bets(user_id, [])
        await interaction.response.send_message("🗑️ Your betslip has been cleared.", ephemeral=True)

    @app_commands.command(name="showoff", description="Show off your betslip to the current channel.")
    async def showoff(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        bets = self.get_user_bets(user_id)

        if not bets:
            await interaction.response.send_message("📭 Your betslip is empty.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"{interaction.user.display_name}'s Betslip 💰",
            color=discord.Color.gold()
        )

        for i, bet in enumerate(bets, 1):
            status_emoji = "✅" if bet["status"] == "won" else "🟡"
            embed.add_field(
                name=f"{i}. {bet['bet']}",
                value=f"Odds: `{bet['odds']}`\nStatus: {status_emoji} {bet['status'].capitalize()}",
                inline=False
            )

        embed.set_footer(text="Feeling lucky? 🍀")

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="showslip", description="Show your current betslip.")
    async def showslip(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        bets = self.get_user_bets(user_id)

        if not bets:
            await interaction.response.send_message("📭 Your betslip is empty.", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"{interaction.user.display_name}'s Betslip",
            color=discord.Color.blue()
        )

        for i, bet in enumerate(bets, 1):
            status_emoji = "✅" if bet["status"] == "won" else "🟡"
            embed.add_field(
                name=f"{i}. {bet['bet']}",
                value=f"Odds: `{bet['odds']}`\nStatus: {status_emoji} {bet['status'].capitalize()}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="win", description="Mark one of your bets as won.")
    @app_commands.describe(bet="The exact bet description to mark as won")
    async def win(self, interaction: discord.Interaction, bet: str):
        user_id = str(interaction.user.id)
        bets = self.get_user_bets(user_id)

        found = False
        for b in bets:
            if b["bet"].lower() == bet.lower():
                b["status"] = "won"
                found = True
                break

        if found:
            self.update_user_bets(user_id, bets)
            await interaction.response.send_message(f"🏆 Bet marked as **won**: {bet}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Bet not found in your betslip.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SportsBetting(bot))
