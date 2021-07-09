import os
import discord
import datetime
import json
import io
import traceback
import textwrap
import inspect
import aiohttp
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import redirect_stdout
from discord.ext import commands
import subprocess
import asyncio
from ext import utils
from ext.paginator import PaginatorSession
intents=discord.Intents.all()
intents.members = True

with open('./setting/config.json', 'r') as cjson:
    config = json.load(cjson)

prefix = config["prefix"]

bot = commands.Bot(command_prefix=prefix,
                   description="Bot utilitaire créé avec la librairie discord py", intents=intents)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(config["token"])
