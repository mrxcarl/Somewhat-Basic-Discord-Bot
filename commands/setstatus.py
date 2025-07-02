import discord
from discord.ext import commands
from discord import app_commands
from config import BOT_OWNER

class SetStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setstatus", description="Set the bot's status and activity.")
    @app_commands.describe(
        activity="What should the bot be doing?",
        type="Type of activity (Playing, Watching, Listening, Competing)",
        status="Bot's online status"
    )
    @app_commands.choices(
        type=[
            app_commands.Choice(name="Playing", value="playing"),
            app_commands.Choice(name="Watching", value="watching"),
            app_commands.Choice(name="Listening", value="listening"),
            app_commands.Choice(name="Competing", value="competing")
        ],
        status=[
            app_commands.Choice(name="Online", value="online"),
            app_commands.Choice(name="Idle", value="idle"),
            app_commands.Choice(name="Do Not Disturb", value="dnd"),
            app_commands.Choice(name="Invisible", value="invisible")
        ]
    )
    async def setstatus(self, interaction: discord.Interaction, activity: str, type: app_commands.Choice[str], status: app_commands.Choice[str]):
        # Check if user is bot owner
        if interaction.user.id != BOT_OWNER:
            await interaction.response.send_message("❌ You are not authorized to use this command.", ephemeral=True)
            return

        # Map status to discord.Status
        status_map = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.do_not_disturb,
            "invisible": discord.Status.invisible
        }

        # Map activity type
        activity_obj = None
        if type.value == "playing":
            activity_obj = discord.Game(name=activity)
        elif type.value == "watching":
            activity_obj = discord.Activity(type=discord.ActivityType.watching, name=activity)
        elif type.value == "listening":
            activity_obj = discord.Activity(type=discord.ActivityType.listening, name=activity)
        elif type.value == "competing":
            activity_obj = discord.Activity(type=discord.ActivityType.competing, name=activity)

        # Set bot presence
        await self.bot.change_presence(status=status_map[status.value], activity=activity_obj)
        await interaction.response.send_message(f"✅ Status updated to **{type.name} {activity}** and **{status.name}**.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SetStatus(bot))
