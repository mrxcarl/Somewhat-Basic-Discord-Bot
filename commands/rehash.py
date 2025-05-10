import discord
from discord.ext import commands
import os
import importlib

class Rehash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Rehash command loaded!")

    @discord.app_commands.command(name="rehash", description="Reload all command modules")
    async def rehash(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need to be an **Administrator** to use this command!", ephemeral=True)
            return

        command_dir = "commands"
        reloaded = []
        failed = []

        for filename in os.listdir(command_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"{command_dir}.{filename[:-3]}"
                try:
                    await self.bot.unload_extension(module_name)  # Unload the module first
                    await self.bot.load_extension(module_name)   # Load it again
                    reloaded.append(filename)
                except Exception as e:
                    failed.append((filename, str(e)))

        embed = discord.Embed(title="🔄 Command Modules Reloaded", color=discord.Color.blue())
        if reloaded:
            embed.add_field(name="✅ Successfully Reloaded:", value="\n".join(reloaded), inline=False)
        if failed:
            embed.add_field(name="❌ Failed to Reload:", value="\n".join([f"{f} - {e}" for f, e in failed]), inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Rehash(bot))
