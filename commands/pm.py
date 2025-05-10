import discord
from discord.ext import commands

class PM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ PM command loaded!")

    @discord.app_commands.command(name="pm", description="Send a private message to a user")
    async def pm(self, interaction: discord.Interaction, user: discord.User, message: str):
        # Append the disclaimer to the message
        message_with_disclaimer = f"{message}\n\n(This bot does not forward private messages)"

        try:
            # Send the private message (DM)
            await user.send(message_with_disclaimer)
            await interaction.response.send_message(f"✅ Sent a private message to {user.mention}!", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"❌ I could not send a private message to {user.mention}. They might have DMs disabled.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(PM(bot))
