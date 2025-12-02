import discord
from discord import app_commands, Interaction
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

load_dotenv()

# create bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD")
guild = discord.Object(id=GUILD_ID)
allowed_user = os.getenv("ALLOWED_USER_ID")

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

@bot.tree.command(name="rps", description="Rock Paper Scissors", guild=guild)
@app_commands.describe(hand="Rock / Paper / Scissors")
async def rps(interaction: Interaction, hand: str):
    hand = hand.lower()
    choices = ["rock", "paper", "scissors"]

    if hand not in choices:
        await interaction.response.send_message(f"> Invalid input: {hand}")
        return

    bot_choice = random.choice(choices)

    if bot_choice == hand:
        result = "Draw!"
    elif (hand == "rock" and bot_choice == "scissors") or (hand == "paper" and bot_choice == "rock") or (hand == "scissors" and bot_choice == "paper"):
        result = "Human won!"
    else:
        result = "Bot won!"

    await interaction.response.send_message(f"> :robot:: {bot_choice.capitalize()}  -  :bust_in_silhouette:: {hand.capitalize()}\n> {result}")

@bot.tree.command(name="random", description="Random number generator (float)", guild=guild)
@app_commands.describe(a="Lowest number", b="Highest number")
async def random_number(interaction: Interaction, a: float, b: float):
    if a >= b:
        await interaction.response.send_message("> First number must be less than the second")
        return
    result = random.randint(a, b)
    await interaction.response.send_message(f"> Result: {result}")

@bot.tree.command(name="token", description="See the bot token.", guild=guild)
async def token(interaction: Interaction):
    if str(interaction.user.id) != str(allowed_user):
        await interaction.response.send_message(f"> You are not allowed to run this command.", ephemeral=True)
        return
    else:
        await interaction.response.send_message(f"> The current bot token is `{TOKEN}`", ephemeral=True)

bot.run(TOKEN)
