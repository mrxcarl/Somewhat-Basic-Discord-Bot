import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
from config import ACCUWEATHER_API_KEY
import asyncio

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_location_key(self, zip_code: str):
        url = f"http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey={ACCUWEATHER_API_KEY}&q={zip_code}&countryCode=US"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                if not data or 'Key' not in data[0]:
                    return None
                return data[0]['Key'], data[0]['LocalizedName']

    async def get_weather(self, location_key: str):
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={ACCUWEATHER_API_KEY}&details=true"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                if not data:
                    return None
                return data[0]

    @app_commands.command(name="weather", description="Get current weather by ZIP code (AccuWeather)")
    @app_commands.describe(zip_code="5-digit US ZIP code")
    async def weather(self, interaction: discord.Interaction, zip_code: str):
        await interaction.response.defer()

        location = await self.get_location_key(zip_code)
        if not location:
            await interaction.followup.send("❌ Invalid ZIP code or failed to find location.", ephemeral=True)
            return

        key, city = location
        weather = await self.get_weather(key)
        if not weather:
            await interaction.followup.send("❌ Could not fetch weather data.", ephemeral=True)
            return

        desc = weather["WeatherText"]
        temp = weather["Temperature"]["Imperial"]["Value"]
        realfeel = weather["RealFeelTemperature"]["Imperial"]["Value"]
        humidity = weather["RelativeHumidity"]
        wind = weather["Wind"]["Speed"]["Imperial"]["Value"]
        icon_number = str(weather["WeatherIcon"]).zfill(2)
        icon_url = f"https://developer.accuweather.com/sites/default/files/{icon_number}-s.png"

        embed = discord.Embed(
            title=f"🌦️ Weather in {city} ({zip_code})",
            description=f"**{desc}**",
            color=discord.Color.teal()
        )
        embed.set_thumbnail(url=icon_url)
        embed.add_field(name="Temperature", value=f"{temp}°F", inline=True)
        embed.add_field(name="Feels Like", value=f"{realfeel}°F", inline=True)
        embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
        embed.add_field(name="Wind Speed", value=f"{wind} mph", inline=True)
        embed.set_footer(text="Powered by AccuWeather")

        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))
