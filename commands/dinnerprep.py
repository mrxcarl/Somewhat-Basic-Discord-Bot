import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from datetime import datetime

# Tracks dinner prep sessions in memory
dinner_sessions = {}  # key: user_id, value: (start_time, meal)

class DinnerPrep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="dinnerprep", description="Start or stop dinner prep status")
    @app_commands.describe(action="Start or stop your dinner prep", meal="What are you cooking?")
    async def dinnerprep(
        self,
        interaction: discord.Interaction,
        action: str,
        meal: str = None
    ):
        user_id = interaction.user.id
        guild = interaction.guild
        channel = discord.utils.get(guild.text_channels, name="general") or interaction.channel

        if action.lower() == "start":
            if user_id in dinner_sessions:
                await interaction.response.send_message("❌ You already started dinner prep!", ephemeral=True)
                return

            start_time = datetime.utcnow()
            dinner_sessions[user_id] = (start_time, meal)

            embed = discord.Embed(
                title="🍽️ Dinner Prep Started!",
                description=f"{interaction.user.mention} is prepping dinner!",
                color=discord.Color.orange()
            )
            if meal:
                embed.add_field(name="🍲 Cooking", value=meal, inline=False)
            embed.set_footer(text=f"Started at {start_time.strftime('%H:%M:%S UTC')}")

            view = CheckTimeView(user_id, start_time)

            await channel.send(embed=embed, view=view)
            await interaction.response.send_message("✅ Dinner prep started!", ephemeral=True)

        elif action.lower() == "done":
            if user_id not in dinner_sessions:
                await interaction.response.send_message("❌ You haven't started dinner prep yet!", ephemeral=True)
                return

            start_time, meal = dinner_sessions.pop(user_id)
            duration = datetime.utcnow() - start_time
            minutes, seconds = divmod(int(duration.total_seconds()), 60)

            embed = discord.Embed(
                title="✅ Dinner Prep Finished!",
                description=f"{interaction.user.mention} has finished prepping dinner!",
                color=discord.Color.green()
            )
            if meal:
                embed.add_field(name="🍲 Meal", value=meal, inline=False)
            embed.add_field(name="⏱️ Duration", value=f"{minutes}m {seconds}s", inline=False)
            embed.set_footer(text=f"Started at {start_time.strftime('%H:%M:%S UTC')}")

            await channel.send(embed=embed)
            await interaction.response.send_message("✅ Dinner prep marked as done.", ephemeral=True)

        else:
            await interaction.response.send_message("❌ Invalid action. Use `start` or `done`.", ephemeral=True)

# View for the check time button
class CheckTimeView(View):
    def __init__(self, user_id, start_time):
        super().__init__(timeout=None)
        self.add_item(CheckTimeButton(user_id, start_time))

class CheckTimeButton(Button):
    def __init__(self, user_id, start_time):
        super().__init__(label="⏱️ Check Time", style=discord.ButtonStyle.blurple)
        self.user_id = user_id
        self.start_time = start_time

    async def callback(self, interaction: discord.Interaction):
        now = datetime.utcnow()
        elapsed = now - self.start_time
        minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
        await interaction.response.send_message(
            f"⏱️ <@{self.user_id}> has been prepping dinner for **{minutes}m {seconds}s**.",
            ephemeral=False
        )

async def setup(bot):
    await bot.add_cog(DinnerPrep(bot))
