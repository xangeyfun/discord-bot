import discord
from discord import app_commands, Interaction
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

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
    await interaction.response.send_message(f"> Pong! {round(bot.latency * 1000)}ms :ping_pong:")


@bot.tree.command(name="calc", description="Simple calculator", guild=guild)
@app_commands.describe(expression="an expression like 5*2+3")
async def calc(interaction: Interaction, expression: str):
    allowed = "0123456789+-*/(). "
    if any(c not in allowed for c in expression):
        await interaction.response.send_message("> invalid expression")
        return
    result = eval(expression)
    await interaction.response.send_message(f"> {expression} = {result}")

@bot.tree.command(name="flip", description="Flip a coin.", guild=guild)
async def flip(interaction: Interaction):
    await interaction.response.send_message("> " + random.choice(["Heads!", "Tails!"]))

@bot.tree.command(name="github", description="Find the code on github!", guild=guild)
async def github(interaction: discord.Interaction):
    await interaction.response.send_message(f"> Bot made by xangey_fun <@996771607630585856>\n> <https://github.com/xangeyfun/discord-bot>")

bot.run(TOKEN)
