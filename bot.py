import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# create bot with intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.getenv("TOKEN")

# when bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Error while syncing commands: {e}")

# a simple slash command
@bot.tree.command(name="ping", description="Test the bot's latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"> Pong! {round(bot.latency * 1000)}ms")

bot.run(TOKEN)
