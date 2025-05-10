import discord
from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Clear command loaded!")

    @discord.app_commands.command(name="clear", description="Clear a specified number of messages")
    async def clear(self, interaction: discord.Interaction, amount: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need to be an **Administrator** to use this command!", ephemeral=True)
            return

        if amount < 1:
            await interaction.response.send_message("❌ Please specify a number greater than 0.", ephemeral=True)
            return

        await interaction.channel.purge(limit=amount + 1)  # +1 to delete the command message itself
        await interaction.response.send_message(f"🧹 Successfully deleted **{amount}** messages.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Clear(bot))
