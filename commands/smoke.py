import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from datetime import datetime
import asyncio

class SmokeView(View):
    def __init__(self, user_id, smoke_sessions):
        super().__init__(timeout=None)
        self.user_id = user_id
        self.smoke_sessions = smoke_sessions

    @discord.ui.button(label="Check Time", style=discord.ButtonStyle.primary)
    async def check_time(self, interaction: discord.Interaction, button: Button):
        start_time = self.smoke_sessions.get(str(self.user_id))
        if not start_time:
            await interaction.response.send_message("❌ This smoke break is already over.", ephemeral=False)
            return

        duration = datetime.utcnow() - start_time
        minutes, seconds = divmod(duration.total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)
        formatted_duration = (
            f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
            if hours > 0 else f"{int(minutes)}m {int(seconds)}s"
        )
        await interaction.response.send_message(f"⏱️ {interaction.user.mention}, they've been gone for `{formatted_duration}`.", ephemeral=False)


class Smoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.smoke_sessions = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Smoke command loaded!")

    @app_commands.command(name="smoke", description="Start or stop a smoke break")
    @app_commands.describe(status="Choose 'on' to start or 'off' to end your break")
    async def smoke(self, interaction: discord.Interaction, status: str):
        user_id = str(interaction.user.id)
        general = discord.utils.get(interaction.guild.text_channels, name="general")

        if status.lower() == "on":
            if user_id in self.smoke_sessions:
                await interaction.response.send_message("🚬 You're already on a smoke break.", ephemeral=True)
                return

            self.smoke_sessions[user_id] = datetime.utcnow()

            embed = discord.Embed(
                title=f"{interaction.user.display_name} is out for a smoke break!",
                description="☁️ They'll be back soon. Click below to check how long they've been gone.",
                color=discord.Color.orange()
            )
            embed.set_footer(text="Smoke break started")
            embed.set_thumbnail(url="https://u.cubeupload.com/mrxcarl/cig.png")

            if general:
                await general.send(embed=embed, view=SmokeView(user_id, self.smoke_sessions))

            await interaction.response.send_message("🚬 Smoke break started.", ephemeral=True)

        elif status.lower() == "off":
            start_time = self.smoke_sessions.get(user_id)
            if not start_time:
                await interaction.response.send_message("🚫 You're not currently on a smoke break.", ephemeral=True)
                return

            duration = datetime.utcnow() - start_time
            minutes, seconds = divmod(duration.total_seconds(), 60)
            hours, minutes = divmod(minutes, 60)
            formatted_duration = (
                f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
                if hours > 0 else f"{int(minutes)}m {int(seconds)}s"
            )

            del self.smoke_sessions[user_id]

            embed = discord.Embed(
                title=f"{interaction.user.display_name} is back!",
                description=f"☁️ Finished their smoke break.\n\n**Duration:** `{formatted_duration}`",
                color=discord.Color.green()
            )
            embed.set_footer(text="Welcome back!")
            embed.set_thumbnail(url="https://u.cubeupload.com/mrxcarl/extcig.png")

            if general:
                await general.send(embed=embed)

            await interaction.response.send_message("🟢 You're marked as back from your break.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Invalid status. Use `/smoke on` or `/smoke off`.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Smoke(bot))
