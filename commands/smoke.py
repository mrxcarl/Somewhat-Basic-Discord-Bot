import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime, timezone, timedelta

DATA_FILE = "smoke_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

class SmokeView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = str(user_id)

@discord.ui.button(label="⏱️ How long?", style=discord.ButtonStyle.primary)
async def how_long(self, interaction: discord.Interaction, button: discord.ui.Button):
    data = load_data()
    if self.user_id in data:
        start_time = datetime.fromisoformat(data[self.user_id])
        now = datetime.now(timezone.utc)
        delta = now - start_time
        mins, secs = divmod(int(delta.total_seconds()), 60)
        hrs, mins = divmod(mins, 60)

        duration_str = f"{hrs}h {mins}m {secs}s" if hrs else f"{mins}m {secs}s"

        user = await interaction.client.fetch_user(int(self.user_id))
        await interaction.response.send_message(
            f"🕒 **{user.display_name}** has been on a smoke break for **{duration_str}**.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message("❌ This user isn't currently on a smoke break.", ephemeral=True)


class Smoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Smoke command loaded!")

    @app_commands.command(name="smoke", description="Announce that you're on or off a smoke break")
    @app_commands.describe(status="Use 'on' to go for a smoke break or 'off' to return.")
    async def smoke(self, interaction: discord.Interaction, status: str):
        status = status.lower()
        member = interaction.user
        guild = interaction.guild
        user_id = str(member.id)

        general = discord.utils.get(guild.text_channels, name="general")
        if not general:
            await interaction.response.send_message("❌ Couldn't find a #general channel.", ephemeral=True)
            return

        data = load_data()

        if status == "on":
            if user_id in data:
                await interaction.response.send_message("🚬 You're already on a smoke break!", ephemeral=True)
                return

            # Log start time
            data[user_id] = datetime.now(timezone.utc).isoformat()
            save_data(data)

            embed = discord.Embed(
                title="🚬 Smoke Break",
                description=f"{member.mention} is stepping out for a smoke.",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url=member.display_avatar.url)

            view = SmokeView(user_id)
            await general.send(embed=embed, view=view)
            await interaction.response.send_message("✅ Smoke break started.", ephemeral=True)

        elif status == "off":
            if user_id not in data:
                await interaction.response.send_message("❌ You weren't on a smoke break.", ephemeral=True)
                return

            # Clear log
            del data[user_id]
            save_data(data)

            embed = discord.Embed(
                title="🟢 Back from Smoke",
                description=f"{member.mention} has returned from their smoke break.",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.display_avatar.url)

            await general.send(embed=embed)
            await interaction.response.send_message("✅ Smoke break ended.", ephemeral=True)

        else:
            await interaction.response.send_message("❌ Use `/smoke on` or `/smoke off`.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Smoke(bot))
