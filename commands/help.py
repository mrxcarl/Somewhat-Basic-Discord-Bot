import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ Help command loaded!")

    @discord.app_commands.command(name="help", description="Lists all available commands with their descriptions")
    async def help(self, interaction: discord.Interaction):
        # Initialize a list to store command names and descriptions
        command_list = []
        
        # Fetch all commands and their descriptions
        for command in self.bot.tree.get_commands():
            command_list.append(f"/{command.name} - {command.description}")

        # Build the embed with all commands and their descriptions
        embed = discord.Embed(
            title="Help - Available Commands",
            description="Here is a list of all available commands with descriptions:",
            color=discord.Color.green()
        )
        embed.add_field(name="Commands", value="\n".join(command_list), inline=False)
        embed.set_footer(text="Use /command_name to run any command!")

        # Send the embed
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
