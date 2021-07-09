import discord
from discord.ext import commands
import json

def setup(client):
     client.add_cog(error(client))

class error(commands.Cog):

        def __init__(self, client):
          self.client = client
        