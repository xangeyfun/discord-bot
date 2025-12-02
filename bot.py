import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready() -> None:
	print(f"Logged in as {client.user}")
	print(f"Token: {TOKEN}")

client.run(TOKEN)
