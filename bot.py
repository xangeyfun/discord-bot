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
guild = discord.Object(id=int(os.getenv("GUILD_ID")))
def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"{date()} DEBUG  Starting bot...\n")

@bot.event
async def on_ready():
    print(f"\n{date()} DEBUG  Logged in as {bot.user}")
    try:
        print(f"{date()} DEBUG  Syncing commands...")
        start_sync = time.time()
        synced = await bot.tree.sync() #guild=guild)
        done = time.time()
    except Exception as e:
        print(f"{date()} ERROR  Error while syncing commands: {e}")
        exit(1)
    total_guilds = len(bot.guilds)
    total_members = sum(guild.member_count for guild in bot.guilds)
    sync_time = f"{done - start_sync:.2f}s"
    print(f"\n{date()} DEBUG  --- Bot is ready! ---")
    print(f"{date()} DEBUG  Invite link: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands")
    print(f"{date()} DEBUG  Connected to {total_guilds} guilds ({total_members} members)")
    print(f"{date()} DEBUG  Synced {len(synced)} slash commands in {sync_time}")
    print(f"{date()} DEBUG  Startup time: {done - startup:.2f} seconds")
    print(f"{date()} DEBUG ---------------------\n")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.application_command:
        guild_name = interaction.guild.name if interaction.guild else "DM"
        channel_name = getattr(interaction.channel, 'name', 'Unknown') if interaction.channel else "Unknown"
        user_name = interaction.user.name if interaction.user else "Unknown"
        command_name = interaction.command.name if interaction.command else "Unknown"

        options_str = ""
        if interaction.data and "options" in interaction.data:
            options = interaction.data["options"]
            parts = []
            for opt in options:
                parts.append(f"{opt['name']}:{opt['value']}")
            options_str = " " + " ".join(parts) if parts else ""

        print(f"{date()} COMMAND '/{command_name}{options_str}' used by {user_name} in {guild_name}/#{channel_name}")


@bot.tree.command(name="help", description="Get help about the bot.") # , guild=guild)
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
        "> `/meme [str]` - Get a random meme.\n"
        "> `/duck` - Get a random duck picture.\n"
        "> `/fox` - Get a random fox picture.\n"
        "> `/uptime` - Check the bot's uptime.\n"
    )
    await interaction.response.send_message(help_text, ephemeral=True)

@bot.tree.command(name="ping", description="Test the bot's latency.") # , guild=guild)
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"> Pong! {round(bot.latency * 1000)}ms :ping_pong:", ephemeral=True)

@bot.tree.command(name="calc", description="Simple calculator") # , guild=guild)
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

@bot.tree.command(name="flip", description="Flip a coin.") # , guild=guild)
@app_commands.describe(hidden="Hide the command from others")
async def flip(interaction: Interaction, hidden: bool = False):
    if hidden:
        await interaction.response.send_message("> " + random.choice(["Heads!", "Tails!"]), ephemeral=True)
    else:
        await interaction.response.send_message("> " + random.choice(["Heads!", "Tails!"]))

@bot.tree.command(name="github", description="Find the code on github!") # , guild=guild)
async def github(interaction: discord.Interaction):
    await interaction.response.send_message(f"> Bot made by xangey_fun <@996771607630585856>\n> <https://github.com/xangeyfun/discord-bot>")

@bot.tree.command(name="rps", description="Rock Paper Scissors") # , guild=guild)
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

@bot.tree.command(name="random", description="Random number generator") # , guild=guild)
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

@bot.tree.command(name="userinfo", description="Get info about a user") # , guild=guild)
@app_commands.describe(user="The user you want info about", hidden="Hide the command from others")
async def userinfo(interaction: discord.Interaction, user: discord.Member, hidden: bool = False):
    roles = [role.name for role in user.roles if role.name != "@everyone"]
    embed = discord.Embed(title=f"{user.name}", color=discord.Color.blue())
    embed.add_field(name="ID", value=user.id)
    embed.add_field(name="Account created", value=user.created_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Joined server", value=user.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Roles", value=", ".join(roles) or "None")
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.set_footer(text=f"Requested by {interaction.user.name} • {datetime.datetime.now()}")
    if hidden:
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="quote", description="Get a quote") # , guild=guild)
@app_commands.describe(choice='"Today" or "Random"', hidden="Hide the command from others")
@app_commands.choices(choice=[
    app_commands.Choice(name="Today", value="Today"),
    app_commands.Choice(name="Random", value="Random")
])
async def quote(interaction: discord.Interaction, choice: str, hidden: bool = False):
    if choice.lower() != "today" and choice.lower() != "random":
        await interaction.response.send_message(f"> Invalid input: {choice}", ephemeral=True)
        return
    try:
        r = requests.get(f"https://zenquotes.io/api/{choice.lower()}")
    except Exception as e:
        await interaction.response.send_message(f"> Could not fetch quote. Please try again later.\nDetails: {e}", ephemeral=True)
        return
    data = r.json()
    if hidden:
        await interaction.response.send_message(f"> \"{data[0]['q']}\" - {data[0]['a']}", ephemeral=True)
    else:
        await interaction.response.send_message(f"> \"{data[0]['q']}\" - {data[0]['a']}")

@bot.tree.command(name="meme", description="Get a random meme") # , guild=guild)
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

@bot.tree.command(name="duck", description="Get a random duck picture") # , guild=guild)
@app_commands.describe(hidden="Hide the command from others")
async def duck(interaction: discord.Interaction, hidden: bool = False):
    try:
        r = requests.get("https://random-d.uk/api/v2/random")
    except Exception as e:
        embed = discord.Embed(title="Error", description="Could not fetch duck image. Please try again later.", color=discord.Color.red())
        embed.add_field(name="Details", value=str(e))
        embed.set_footer(text=f"{datetime.datetime.now()}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    data = r.json()
    embed = discord.Embed(title="Random Duck", color=discord.Color.blue())
    embed.set_image(url=data['url'])
    if hidden:
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="fox", description="Get a random fox picture") # , guild=guild)
@app_commands.describe(hidden="Hide the command from others")
async def fox(interaction: discord.Interaction, hidden: bool = False):
    try:
        r = requests.get("https://randomfox.ca/floof/")
    except Exception as e:
        embed = discord.Embed(title="Error", description="Could not fetch fox image. Please try again later.", color=discord.Color.red())
        embed.add_field(name="Details", value=str(e))
        embed.set_footer(text=f"{datetime.datetime.now()}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    data = r.json()
    embed = discord.Embed(title="Random Fox", color=discord.Color.orange())
    embed.set_image(url=data['image'])
    if hidden:
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="uptime", description="Check the bot's uptime.") # , guild=guild)
async def uptime(interaction: discord.Interaction):
    current_time = time.time()
    uptime_seconds = int(current_time - startup)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"
    await interaction.response.send_message(f"> Uptime: {uptime_str}", ephemeral=True)

@bot.tree.command(name="fact", description="Get a daily fact.")# )# , guild=guild)
@app_commands.describe(hidden="Hide the command from others", choice='"Today" or "Random"')
@app_commands.choices(choice=[
    app_commands.Choice(name="Today", value="Today"),
    app_commands.Choice(name="Random", value="Random")
])
async def fact(interaction: discord.Interaction, choice: str, hidden: bool = False):
    if choice.lower() != "today" and choice.lower() != "random":
        await interaction.response.send_message(f"> Invalid input: {choice}", ephemeral=True)
        return
    try:
        r = requests.get(f"https://uselessfacts.jsph.pl/{'today' if choice.lower() == 'today' else 'random'}.json?language=en")
    except Exception as e:
        await interaction.response.send_message(f"> Could not fetch fact. Please try again later.\nDetails: {e}", ephemeral=True)
        return
    data = r.json()
    if hidden:
        await interaction.response.send_message(f"> {data['text']}", ephemeral=True)
    else:
        await interaction.response.send_message(f"> {data['text']}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if any(word in message.content.lower() for word in ["duck", "quack"]):
        await message.add_reaction("🦆")
        await message.channel.send("Quack! 🦆")
        return
    
    if isinstance(message.channel, discord.DMChannel):
        await message.channel.send("Hello! I'm a bot. Please use slash commands to interact with me. Type /help to see available commands.")
        return
    
    await bot.process_commands(message)

bot.run(TOKEN)