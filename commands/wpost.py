import discord
from discord.ext import commands
from discord import app_commands

class WelcomePoster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ WelcomePoster command loaded!")

    @app_commands.command(name="wpost", description="Post a welcome message in the welcome/welcome-and-rules channel")
    @app_commands.describe(owner="The server owner's user mention or name")
    async def wpost(self, interaction: discord.Interaction, owner: str):
        guild = interaction.guild
        welcome_channel = None

        # Try finding a suitable welcome channel by common names
        possible_names = ["welcome", "welcome-and-rules", "welcome-rules", "👋welcome", "👋│welcome"]
        for channel in guild.text_channels:
            if any(name in channel.name.lower() for name in possible_names):
                welcome_channel = channel
                break

        if not welcome_channel:
            await interaction.response.send_message("❌ No suitable welcome channel found (e.g., 'welcome', 'welcome-and-rules').", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"👋 Welcome to **{guild.name}**!",
            description=(
                f"We're excited to have you here! 🎉\n"
                f"This server is owned by **{owner}** and built for community, conversation, and connection.\n\n"
                f"Please make sure to read any rules and say hi in the chat!"
            ),
            color=discord.Color.blurple()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else discord.Embed.Empty)
        embed.set_footer(text="Enjoy your stay!")

        await welcome_channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Welcome message posted in {welcome_channel.mention}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(WelcomePoster(bot))
