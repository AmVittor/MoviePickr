from discord.ext import commands
import discord
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


def setup_gerais(bot):
    @bot.command()
    async def ola(ctx):
        nome = ctx.author.nick or ctx.author.name
        await ctx.reply(f"Olá {nome}")
