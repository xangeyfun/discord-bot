import discord
from discord import app_commands, Interaction
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import requests
import datetime
import time
import ast

startup = time.time()

load_dotenv()

# create bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Type / for commands"))
TOKEN = os.getenv("TOKEN")
allowed_user = os.getenv("ALLOWED_USER_ID")
guild = discord.Object(id=os.getenv("GUILD_ID"))
print("Bot is starting...")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        print("Syncing commands...")
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} slash commands")
        done = time.time()
        print(f"Startup time: {done - startup:.2f} seconds")
    except Exception as e:
        print(f"Error while syncing commands: {e}")
        exit(1)

@bot.tree.command(name="help", description="Get help about the bot.", guild=guild)
async def help(interaction: discord.Interaction):
    help_text = (
        "## **Available Commands:**\n"
        "> **<required>**  |  **[optional]**\n\n"
        "> `/ping` - Test the bot's latency.\n"
        "> `/calc <expression>` - Simple calculator.\n"
        "> `/flip` - Flip a coin.\n"
        "> `/github` - Find the code on GitHub.\n"
        "> `/rps <str>` - Play Rock Paper Scissors.\n"
        "> `/random <int> <int>` - Generate a random number between a and b.\n"
        "> `/userinfo <str>` - Get info about a user.\n"
        "> `/quote <str>` - Get a quote (Today or Random).\n"
        "> `/meme [str] [bool]` - Get a random meme.\n"
    )
    await interaction.response.send_message(help_text, ephemeral=True)

@bot.tree.command(name="ping", description="Test the bot's latency.", guild=guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"> Pong! {round(bot.latency * 1000)}ms :ping_pong:", ephemeral=True)

@bot.tree.command(name="calc", description="Simple calculator", guild=guild)
@app_commands.describe(expression="an expression like 5*2+3")
async def calc(interaction: Interaction, expression: str):
    allowed = "0123456789+-*/(). "
    if any(c not in allowed for c in expression):
        await interaction.response.send_message("> invalid expression", ephemeral=True)
        return
    try:
        result = ast.literal_eval(expression)
        await interaction.response.send_message(f"> `{expression}` = {result}", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"> Error evaluating expression: {e}", ephemeral=True)

@bot.tree.command(name="flip", description="Flip a coin.", guild=guild)
@app_commands.describe(hidden="Hide the command from others")
async def flip(interaction: Interaction, hidden: bool = False):
    if hidden:
        await interaction.response.send_message("> " + random.choice(["Heads!", "Tails!"]), ephemeral=True)
    else:
        await interaction.response.send_message("> " + random.choice(["Heads!", "Tails!"]))

@bot.tree.command(name="github", description="Find the code on github!", guild=guild)
async def github(interaction: discord.Interaction):
    await interaction.response.send_message(f"> Bot made by xangey_fun <@996771607630585856>\n> <https://github.com/xangeyfun/discord-bot>")

@bot.tree.command(name="rps", description="Rock Paper Scissors", guild=guild)
@app_commands.describe(hand="Rock / Paper / Scissors", hidden="Hide the command from others")
@app_commands.choices(hand=[
    app_commands.Choice(name="Rock", value="Rock"),
    app_commands.Choice(name="Paper", value="Paper"),
    app_commands.Choice(name="Scissors", value="Scissors")
])
async def rps(interaction: Interaction, hand: str, hidden: bool = False):
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
    if hidden:
        await interaction.response.send_message(f"> :robot: {bot_choice.capitalize()}  -  :bust_in_silhouette: {hand.capitalize()}\n> {result}", ephemeral=True)
    else:
        await interaction.response.send_message(f"> :robot: {bot_choice.capitalize()}  -  :bust_in_silhouette: {hand.capitalize()}\n> {result}")

@bot.tree.command(name="random", description="Random number generator (float)", guild=guild)
@app_commands.describe(a="Lowest number", b="Highest number", hidden="Hide the command from others")
async def random_number(interaction: Interaction, a: float, b: float, hidden: bool = False):
    if a >= b:
        await interaction.response.send_message("> First number must be less than the second", ephemeral=True)
        return
    result = random.randint(a, b)
    if hidden:
        await interaction.response.send_message(f"> Result: {result}", ephemeral=True)
    else:
        await interaction.response.send_message(f"> Result: {result}")

@bot.tree.command(name="userinfo", description="Get info about a user", guild=guild)
@app_commands.describe(user="The user you want info about", hidden="Hide the command from others")
async def userinfo(interaction: discord.Interaction, user: discord.Member, hidden: bool = False):
    roles = [role.name for role in user.roles if role.name != "@everyone"]
    embed = discord.Embed(title=f"{user.name}", color=discord.Color.blue())
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Joined server", value=user.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Roles", value=", ".join(roles) or "None")
    if hidden:
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="quote", description="Get a quote", guild=guild)
@app_commands.describe(choice='"Today" or "Random"', hidden="Hide the command from others")
@app_commands.choices(choice=[
    app_commands.Choice(name="Today", value="Today"),
    app_commands.Choice(name="Random", value="Random")
])
async def quote(interaction: discord.Interaction, choice: str, hidden: bool = False):
    if choice.lower() != "today" and choice.lower() != "random":
        await interaction.response.send_message(f"> Invalid input: {choice}", ephemeral=True)
        return

    await interaction.response.defer()
    r = requests.get(f"https://zenquotes.io/api/{choice.lower()}")
    print(f"Request response: {r.text}")
    data = r.json()
    if hidden:
        await interaction.followup.send(f"> \"{data[0]['q']}\" - {data[0]['a']}", ephemeral=True)
    else:
        await interaction.followup.send(f"> \"{data[0]['q']}\" - {data[0]['a']}")

@bot.tree.command(name="meme", description="Get a random meme", guild=guild)
@app_commands.describe(subreddit="Subreddit to get meme from (optional)", hidden="Hide the command from others")
async def meme(interaction: discord.Interaction, subreddit: str = None, hidden: bool = False):
    if subreddit == "Examples":
        embed = discord.Embed(title="Meme Subreddit Examples", description="Here are some example subreddits you can use:\n- memes\n- dankmemes\n- wholesomememes\n- me_irl\n- linuxmemes\n- programmerhumor", color=discord.Color.blue())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    url = f"https://meme-api.com/gimme/{subreddit}" if subreddit else "https://meme-api.com/gimme"
    try:
        r = requests.get(url)
    except Exception as e:
        embed = discord.Embed(title="Error", description="Could not fetch meme. Please try again later.", color=discord.Color.red())
        embed.add_field(name="Details", value=str(e))
        embed.set_footer(text=f"{datetime.datetime.now()}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if r.status_code != 200:
        embed = discord.Embed(title="Error", description="Could not fetch meme. Please try again later.", color=discord.Color.red())
        embed.add_field(name="Details", value=f"Status code: {r.status_code}")
        embed.set_footer(text=f"{datetime.datetime.now()}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    data = r.json()
    embed = discord.Embed(title=data['title'], url=data['postLink'], color=discord.Color.green())
    embed.set_image(url=data['url'])
    embed.set_footer(text=f"{datetime.datetime.now()} - From r/{data['subreddit']}")
    if hidden:
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed)

bot.run(TOKEN)