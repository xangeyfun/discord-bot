import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)


@bot.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return

    if message.content == "Hello":
        await message.channel.send("Hi")

    await bot.process_commands(message)

@bot.command()
async def ping(ctx: commands.Context) -> None:
    await ctx.send(f"> Pong! {round(bot.latency * 1000)}ms")

client.run(TOKEN)
