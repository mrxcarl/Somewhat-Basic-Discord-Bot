import discord
from discord.ext import commands

class Nickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Nickname command loaded!")

    @discord.app_commands.command(name="nickname", description="Change the bot's nickname")
    async def nickname(self, interaction: discord.Interaction, new_nickname: str):
        # Check if the user has Administrator permissions
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need to be an **Administrator** to use this command!", ephemeral=True)
            return

        # Check if the bot has permission to change its nickname
        bot_member = interaction.guild.get_member(self.bot.user.id)
        if bot_member.guild_permissions.manage_nicknames:
            try:
                # Change the bot's nickname
                await bot_member.edit(nick=new_nickname)
                await interaction.response.send_message(f"✅ Bot's nickname has been changed to **{new_nickname}**.", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("❌ I do not have permission to change my nickname!", ephemeral=True)
        else:
            await interaction.response.send_message("❌ I do not have permission to change my nickname!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Nickname(bot))
