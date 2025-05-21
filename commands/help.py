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
        await interaction.response.defer()

        try:
            command_list = []
            prefix_commands = []

            # Slash commands
            for command in self.bot.tree.get_commands():
                command_list.append(f"/{command.name} - {command.description}")

            # Prefix commands
            for command in self.bot.commands:
                if isinstance(command, commands.Command):
                    prefix_commands.append(f"!{command.name} - {command.help or 'No description'}")

            all_commands = sorted(command_list + prefix_commands)

            # Build embed
            embed = discord.Embed(
                title="Help - Available Commands",
                description="Here is a list of all available commands with descriptions:",
                color=discord.Color.green()
            )

            # Split the command list into fields of <= 1024 characters
            field_value = ""
            field_count = 1
            for cmd in all_commands:
                if len(field_value) + len(cmd) + 1 > 1024:
                    embed.add_field(name=f"Commands ({field_count})", value=field_value, inline=False)
                    field_value = ""
                    field_count += 1
                field_value += cmd + "\n"
            if field_value:
                embed.add_field(name=f"Commands ({field_count})", value=field_value, inline=False)

            embed.set_footer(text="Use /command_name or !command_name to run any command!")

            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"Error occurred: {e}")
            await interaction.followup.send("❌ Something went wrong generating the help list.")

async def setup(bot):
    await bot.add_cog(Help(bot))
