import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from datetime import datetime, timedelta

class Alarm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.alarms = {}  # key: user_id, value: list of (end_time, reason)

    @app_commands.command(name="alarm", description="Set a reminder/alarm.")
    @app_commands.describe(
        minutes="How many minutes until the alarm goes off",
        reason="What is the alarm for? (Optional)"
    )
    async def alarm(self, interaction: discord.Interaction, minutes: int, reason: str = "No reason provided"):
        if minutes <= 0:
            await interaction.response.send_message("❌ Minutes must be greater than 0.", ephemeral=True)
            return

        user_id = interaction.user.id
        end_time = datetime.utcnow() + timedelta(minutes=minutes)

        # Store the alarm (not persistent across restarts)
        if user_id not in self.alarms:
            self.alarms[user_id] = []
        self.alarms[user_id].append((end_time, reason))

        # Response Embed
        embed = discord.Embed(
            title="⏰ Alarm Set!",
            description=f"**{interaction.user.mention}**, your alarm for:\n**{reason}**\nwill go off in **{minutes} minute(s)**.",
            color=discord.Color.orange()
        )
        embed.set_footer(text=f"Alarm set at {datetime.utcnow().strftime('%H:%M:%S UTC')}")

        await interaction.response.send_message(embed=embed)

        # Wait and alert
        await asyncio.sleep(minutes * 60)

        # DM the user and tag in channel
        try:
            dm_embed = discord.Embed(
                title="🔔 Alarm Time!",
                description=f"⏰ Your alarm for **{reason}** has gone off!",
                color=discord.Color.green()
            )
            dm_embed.set_footer(text="This is your reminder.")

            await interaction.user.send(embed=dm_embed)
        except discord.Forbidden:
            await interaction.followup.send(f"🔔 {interaction.user.mention} your alarm for **{reason}** is up!", ephemeral=False)

        # Clean up stored alarm
        self.alarms[user_id] = [a for a in self.alarms[user_id] if a[0] != end_time]
        if not self.alarms[user_id]:
            del self.alarms[user_id]

async def setup(bot):
    await bot.add_cog(Alarm(bot))
