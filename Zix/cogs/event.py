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
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType
import subprocess
import asyncio
from ext import utils
from ext.paginator import PaginatorSession
from discord.ext.commands import cooldown, BucketType

def setup(client):
     client.add_cog(event(client))

class event(commands.Cog):

        def __init__(self, client):
          self.client = client
        
        @commands.Cog.listener()
        async def on_ready(self):
         DiscordComponents(self.client)
         await self.client.change_presence(status=discord.Status.idle, activity=discord.Game("!help"))
         print("☑️   Zix est prêt !")
        
        @commands.Cog.listener()
        async def on_member_join(self, member):
           join_role = discord.utils.get(member.guild.roles, name='🔰 Petit Nouveau')
           await member.add_roles(join_role)
           channel = member.guild.get_channel(861272478663835648)
           embed = discord.Embed(title=f'Nouvelle Arrivant', description=f'Bienvenue {member.mention}, sur le Hub Nocturne', color=discord.Color.blurple())
           #embed.set_thumbnail(url='https://emoji.gg/assets/emoji/3916-blurple-plane.png')
           await channel.send(embed=embed)
