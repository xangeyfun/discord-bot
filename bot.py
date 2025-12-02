import discord
from discord import app_commands, Interaction
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# create bot with intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD")
guild = discord.Object(id=GUILD_ID)

# when bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Error while syncing commands: {e}")

# a simple slash command
@bot.tree.command(name="ping", description="Test the bot's latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"> Pong! {round(bot.latency * 1000)}ms")


@bot.tree.command(name="calc", description="Simple calculator", guild=guild)
@app_commands.describe(a="first number", o="operator (+ - * /)", b="second number")
async def calc(interaction: Interaction, a: float, o: str, b: float):
    if o == "+":
        result = a + b
    elif o == "-":
        result = a - b
    elif o == "*":
        result = a * b
    elif o == "/":
        result = a / b if b != 0 else "undefined (division by 0)"
    else:
        result = "invalid operator"

    await interaction.response.send_message(f"{a} {o} {b} = {result}")

bot.run(TOKEN)
