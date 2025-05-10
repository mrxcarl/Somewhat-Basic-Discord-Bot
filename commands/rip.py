import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import io
import requests

class RIP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("✅ RIP command loaded!")

    @app_commands.command(name="rip", description="Create a RIP tombstone image with a user's avatar.")
    async def rip(self, interaction: discord.Interaction, user: discord.Member = None):
        user = user or interaction.user

        await interaction.response.defer()  # Acknowledge the command

        # Load base image
        base = Image.open("rip_template.png").convert("RGBA")

        # Download user avatar
        avatar_asset = user.avatar or user.default_avatar
        avatar_url = avatar_asset.replace(size=128).url
        response = requests.get(avatar_url)
        avatar = Image.open(io.BytesIO(response.content)).convert("RGBA").resize((120, 120))

        # Paste avatar onto tombstone
        base.paste(avatar, (115, 115), avatar)

        # Optional: Draw their name on the image
        draw = ImageDraw.Draw(base)
        font = ImageFont.truetype("arial.ttf", 20)  # Use a basic font; ensure it's installed
        draw.text((100, 250), f"RIP {user.display_name}", font=font, fill="black")

        # Save to in-memory file
        with io.BytesIO() as image_binary:
            base.save(image_binary, 'PNG')
            image_binary.seek(0)
            file = discord.File(fp=image_binary, filename="rip.png")
            await interaction.followup.send(content=f"🪦 RIP {user.mention}", file=file)

async def setup(bot):
    await bot.add_cog(RIP(bot))
