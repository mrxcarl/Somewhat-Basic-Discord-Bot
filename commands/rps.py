import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os

STATS_FILE = "rps_stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)

class RPSButton(discord.ui.Button):
    def __init__(self, label, emoji, user_id):
        super().__init__(label=label, emoji=emoji, style=discord.ButtonStyle.primary)
        self.choice = label.lower()
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        view: RPSView = self.view
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ This isn't your button!", ephemeral=True)
            return

        view.choices[self.user_id] = self.choice
        await interaction.response.send_message(f"✅ You chose **{self.choice.title()}**!", ephemeral=True)

        if len(view.choices) == 2:
            await view.finish_game()

class RPSView(discord.ui.View):
    def __init__(self, player1: discord.Member, player2: discord.Member, channel):
        super().__init__(timeout=60)
        self.player1 = player1
        self.player2 = player2
        self.channel = channel
        self.choices = {}

        for player in (player1, player2):
            for label, emoji in [("Rock", "✊"), ("Paper", "✋"), ("Scissors", "✌️")]:
                self.add_item(RPSButton(label=label, emoji=emoji, user_id=player.id))

    async def finish_game(self):
        p1_choice = self.choices[self.player1.id]
        p2_choice = self.choices[self.player2.id]

        result = self.determine_winner(p1_choice, p2_choice)
        stats = load_stats()

        def update_stats(winner_id, loser_id):
            if str(winner_id) not in stats:
                stats[str(winner_id)] = {"wins": 0, "losses": 0}
            if str(loser_id) not in stats:
                stats[str(loser_id)] = {"wins": 0, "losses": 0}
            stats[str(winner_id)]["wins"] += 1
            stats[str(loser_id)]["losses"] += 1
            save_stats(stats)

        embed = discord.Embed(title="✊✋✌️ Rock-Paper-Scissors Result", color=discord.Color.green())
        embed.add_field(name=self.player1.display_name, value=p1_choice.title(), inline=True)
        embed.add_field(name=self.player2.display_name, value=p2_choice.title(), inline=True)

        if result == 0:
            embed.description = "🤝 It's a tie!"
        elif result == 1:
            embed.description = f"🏆 {self.player1.mention} wins!"
            update_stats(self.player1.id, self.player2.id)
        else:
            embed.description = f"🏆 {self.player2.mention} wins!"
            update_stats(self.player2.id, self.player1.id)

        await self.channel.send(embed=embed)
        self.stop()

    def determine_winner(self, choice1, choice2):
        beats = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
        if choice1 == choice2:
            return 0
        elif beats[choice1] == choice2:
            return 1
        else:
            return 2

class RPS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rps", description="Challenge another user to Rock-Paper-Scissors!")
    async def rps(self, interaction: discord.Interaction, opponent: discord.Member):
        if opponent.bot:
            await interaction.response.send_message("🤖 You can't play against a bot!", ephemeral=True)
            return

        if opponent == interaction.user:
            await interaction.response.send_message("😅 You can't challenge yourself!", ephemeral=True)
            return

        view = RPSView(interaction.user, opponent, interaction.channel)

        await interaction.response.send_message(
            f"🎮 {interaction.user.mention} has challenged {opponent.mention} to Rock-Paper-Scissors! Choose your move:",
            view=view
        )

    @app_commands.command(name="rpsstats", description="Check your Rock-Paper-Scissors stats.")
    async def rpsstats(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user
        stats = load_stats()
        data = stats.get(str(user.id), {"wins": 0, "losses": 0})

        embed = discord.Embed(
            title=f"📊 RPS Stats for {user.display_name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Wins", value=str(data["wins"]), inline=True)
        embed.add_field(name="Losses", value=str(data["losses"]), inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(RPS(bot))
