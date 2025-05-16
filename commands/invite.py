import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Invite command loaded!")

    @discord.app_commands.command(name="invite", description="Get an invite link to add the bot to your server.")
    async def invite(self, interaction: discord.Interaction):
        bot_id = self.bot.user.id
        permissions = discord.Permissions(administrator=True)  # or customize if needed

        invite_url = discord.utils.oauth_url(
            client_id=bot_id,
            permissions=permissions,
            scopes=("bot", "applications.commands")
        )

        embed = discord.Embed(
            title="🔗 Invite Me!",
            description=f"[Click here to invite this bot to your server!]({invite_url})",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Invite(bot))
