import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Utility commands loaded!")

    @discord.app_commands.command(name="userinfo", description="Get information about a user.")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user  # Default to the command invoker if no user is given

        embed = discord.Embed(
            title=f"User Info - {user}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        embed.add_field(name="🆔 User ID", value=user.id, inline=False)
        embed.add_field(name="📛 Username", value=user.name, inline=True)
        embed.add_field(name="🏷️ Display Name", value=user.display_name, inline=True)
        embed.add_field(name="🗓️ Account Created", value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name="🔔 Joined Server", value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S') if user.joined_at else "N/A", inline=False)
        embed.add_field(name="👑 Top Role", value=user.top_role.mention if user.top_role else "None", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
