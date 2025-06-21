import discord
from discord.ext import commands
from discord import app_commands

class Imitate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="imitate", description="Send a message that looks like it's from another user using a webhook.")
    @app_commands.describe(user="The user to imitate", message="The message to send")
    async def imitate(self, interaction: discord.Interaction, user: discord.Member, message: str):
        # Check for permissions
        if not interaction.channel.permissions_for(interaction.guild.me).manage_webhooks:
            await interaction.response.send_message("❌ I don't have permission to manage webhooks in this channel.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)  # Optional: hides command processing

        try:
            # Create a webhook
            webhook = await interaction.channel.create_webhook(name="Imitator")
            # Send the message as the user
            await webhook.send(
                content=message,
                username=user.display_name,
                avatar_url=user.display_avatar.url,
            )
            # Clean up
            await webhook.delete()
            await interaction.followup.send(f"✅ Message sent as {user.display_name}!", ephemeral=True)

        except Exception as e:
            await interaction.followup.send("❌ Failed to send the message.", ephemeral=True)
            print(f"[IMITATE ERROR] {e}")

async def setup(bot):
    await bot.add_cog(Imitate(bot))
