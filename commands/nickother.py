import discord
from discord.ext import commands

class NickOther(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ NickOther command loaded!")

    @discord.app_commands.command(name="nickother", description="Change another member's nickname.")
    @discord.app_commands.describe(member="The member whose nickname you want to change", nickname="The new nickname")
    async def nickother(self, interaction: discord.Interaction, member: discord.Member, nickname: str):
        # Permission check
        if not interaction.user.guild_permissions.manage_nicknames:
            await interaction.response.send_message("❌ You don't have permission to manage nicknames.", ephemeral=True)
            return

        # Prevent changing the nickname of someone with a higher or equal role
        if member.top_role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
            await interaction.response.send_message("⚠️ You can't change the nickname of someone with an equal or higher role.", ephemeral=True)
            return

        try:
            await member.edit(nick=nickname, reason=f"Changed by {interaction.user}")
            await interaction.response.send_message(f"✅ Changed {member.mention}'s nickname to **{nickname}**.")
        except discord.Forbidden:
            await interaction.response.send_message("❌ I don't have permission to change that user's nickname.", ephemeral=True)
        except discord.HTTPException:
            await interaction.response.send_message("❌ Failed to change nickname due to an unknown error.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(NickOther(bot))
