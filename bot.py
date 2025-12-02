import discord
from discord import app_commands, Interaction
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import requests

load_dotenv()

# create bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, status=discord.Status.online, activity=discord.Game("Type / for commands"))
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

@bot.tree.command(name="help", description="Get help about the bot.", guild=guild)
async def help(interaction: discord.Interaction):
    help_text = (
        "> **Available Commands:**\n"
        "> `/ping` - Test the bot's latency.\n"
        "> `/calc <expression>` - Simple calculator.\n"
        "> `/flip` - Flip a coin.\n"
        "> `/github` - Find the code on GitHub.\n"
        "> `/rps <hand>` - Play Rock Paper Scissors.\n"
        "> `/random <a> <b>` - Generate a random number between a and b.\n"
        "> `/token` - See the bot token (restricted).\n"
        "> `/userinfo <user>` - Get info about a user.\n"
        "> `/quote <choice>` - Get a quote (Today or Random).\n"
    )
    await interaction.response.send_message(help_text)

# a simple slash command
@bot.tree.command(name="ping", description="Test the bot's latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"> Pong! {round(bot.latency * 1000)}ms :ping_pong:")


@bot.tree.command(name="calc", description="Simple calculator", guild=guild)
@app_commands.describe(expression="an expression like 5*2+3")
async def calc(interaction: Interaction, expression: str):
    allowed = "0123456789+-*/(). "
    if any(c not in allowed for c in expression):
        await interaction.response.send_message("> invalid expression", ephemeral=True)
        return
    try:
        result = eval(expression)
        await interaction.response.send_message(f"> `{expression}` = {result}")
    except Exception as e:
        await interaction.response.send_message(f"> Error evaluating expression: {e}", ephemeral=True)

@bot.tree.command(name="flip", description="Flip a coin.", guild=guild)
async def flip(interaction: Interaction):
    await interaction.response.send_message("> " + random.choice(["Heads!", "Tails!"]))

@bot.tree.command(name="github", description="Find the code on github!", guild=guild)
async def github(interaction: discord.Interaction):
    await interaction.response.send_message(f"> Bot made by xangey_fun <@996771607630585856>\n> <https://github.com/xangeyfun/discord-bot>")

@bot.tree.command(name="rps", description="Rock Paper Scissors", guild=guild)
@app_commands.describe(hand="Rock / Paper / Scissors")
@app_commands.choices(hand=[
    app_commands.Choice(name="Rock", value="Rock"),
    app_commands.Choice(name="Paper", value="Paper"),
    app_commands.Choice(name="Siccors", value="Siccors")
])
async def rps(interaction: Interaction, hand: str):
    hand = hand.lower()
    choices = ["rock", "paper", "scissors"]

    if hand not in choices:
        await interaction.response.send_message(f"> Invalid input: {hand}", ephemeral=True)
        return

    bot_choice = random.choice(choices)

    if bot_choice == hand:
        result = "Draw!"
    elif (hand == "rock" and bot_choice == "scissors") or (hand == "paper" and bot_choice == "rock") or (hand == "scissors" and bot_choice == "paper"):
        result = "Human won!"
    else:
        result = "Bot won!"

    await interaction.response.send_message(f"> :robot: {bot_choice.capitalize()}  -  :bust_in_silhouette: {hand.capitalize()}\n> {result}")

@bot.tree.command(name="random", description="Random number generator (float)", guild=guild)
@app_commands.describe(a="Lowest number", b="Highest number")
async def random_number(interaction: Interaction, a: float, b: float):
    if a >= b:
        await interaction.response.send_message("> First number must be less than the second", ephemeral=True)
        return
    result = random.randint(a, b)
    await interaction.response.send_message(f"> Result: {result}")

@bot.tree.command(name="token", description="See the bot token.", guild=guild)
async def token(interaction: Interaction):
    if str(interaction.user.id) != str(allowed_user):
        await interaction.response.send_message(f"> You are not allowed to run this command.", ephemeral=True)
        return
    else:
        masked = (TOKEN[:16] + "*" * (len(TOKEN) - 8) + TOKEN[-16:]) if TOKEN else "no token set"
        await interaction.response.send_message(f"> The current bot token is\n> `{masked}`", ephemeral=True)

@bot.tree.command(name="userinfo", description="Get info about a user", guild=guild)
@app_commands.describe(user="The user you want info about")
async def userinfo(interaction: discord.Interaction, user: discord.Member):
    roles = [role.name for role in user.roles if role.name != "@everyone"]
    embed = discord.Embed(title=f"{user.name}", color=discord.Color.blue())
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Joined server", value=user.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Roles", value=", ".join(roles) or "None")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="quote", description="Get a qoute", guild=guild)
@app_commands.describe(choice='"Today" or "Random"')
@app_commands.choices(choice=[
    app_commands.Choice(name="Today", value="Today"),
    app_commands.Choice(name="Random", value="Random")
])
async def qoute(interaction: discord.Interaction, choice: str):
    if choice.lower() != "today" and choice.lower() != "random":
        await interaction.response.send_message(f"> Invalid input: {choice}", ephemeral=True)
        return

    await interaction.response.defer()
    r = requests.get(f"https://zenquotes.io/api/{choice.lower()}")
    print(f"Request response: {r.text}")
    data = r.json()
    await interaction.followup.send(f"> \"{data[0]['q']}\" - {data[0]['a']}")

bot.run(TOKEN)
