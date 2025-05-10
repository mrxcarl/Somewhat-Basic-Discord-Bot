import discord
from discord.ext import commands

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ About command loaded!")

    @discord.app_commands.command(name="about", description="Information about the bot and its creator")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="About This Bot",
            description="This bot was created to make your Discord experience more fun and interactive. 🚀",
            color=discord.Color.blue()
        )

        # Customize the details about the creator
        embed.add_field(
            name="Creator",
            value="**Jason Klein**\nA developer who loves building bots and automating tasks on Discord. 😊",
            inline=False
        )

        # You can add links to social media or repositories
        embed.add_field(
            name="Links",
            value="[GitHub](https://github.com/mrxcarl)",
            inline=False
        )

        embed.add_field(
            name="Bot Purpose",
            value="This bot is designed to provide entertainment, utility, and ease of use with commands like memes, dice rolls, and more!",
            inline=False
        )

        embed.set_footer(text="Thanks for using the bot! 😊")

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(About(bot))
