import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from comandos.gerais import setup_gerais
from comandos.filmes import setup_filmes

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print("Bot inicializado!")

# Registra os comandos dos arquivos separados
setup_gerais(bot)
setup_filmes(bot)

bot.run(token)
