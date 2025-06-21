import discord
from discord.ext import commands
from discord import app_commands

class EmbedMaker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="embed", description="Send a fancy embedded message to this channel.")
    @app_commands.describe(
        title="The title of the embed",
        description="The main body of the embed message",
        color="Hex color code (e.g. #00ff00). Leave empty for default.",
        footer="Optional footer text"
    )
    async def embed(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        color: str = None,
        footer: str = None
    ):
        try:
            # Convert hex color to int
            embed_color = discord.Color.default()
            if color:
                color = color.lstrip("#")
                embed_color = discord.Color(int(color, 16))

            # Create embed
            embed = discord.Embed(
                title=title,
                description=description,
                color=embed_color
            )
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            if footer:
                embed.set_footer(text=footer)

            await interaction.response.send_message("✅ Embed sent!", ephemeral=True)
            await interaction.channel.send(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to create embed: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(EmbedMaker(bot))
