import discord
from discord.ext import commands

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Announce command loaded!")

    @discord.app_commands.command(name="announce", description="Send an embedded announcement to the announcements channel (Admin only)")
    @commands.has_permissions(administrator=True)
    async def announce(self, interaction: discord.Interaction, title: str, message: str):
        """Send an announcement as an embed to the announcements channel."""
        
        # Find the announcements channel in the guild
        announcements_channel = discord.utils.get(interaction.guild.text_channels, name="announcements")
        
        if not announcements_channel:
            await interaction.response.send_message("⚠️ No 'announcements' channel found. Please create one or specify a channel.", ephemeral=True)
            return
        
        # Create the embed
        embed = discord.Embed(
            title=f"📢 {title}",
            description=f"**{message}**",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/561/561127.png")  # Optional icon
        embed.set_footer(text=f"📣 Announced by {interaction.user.display_name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
        
        # Send the embed to the announcements channel
        await announcements_channel.send(embed=embed)
        await interaction.response.send_message("✅ Announcement sent!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Announce(bot))
