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

with open('./setting/config.json', 'r') as cjson:
    config = json.load(cjson)

with open('./setting/role.json', 'r') as cjson:
    role = json.load(cjson)

def setup(client):
     client.add_cog(admin(client))

class admin(commands.Cog):
    '''Commandes de gestion d'adminstration'''

    def __init__(self, client):
        self.client = client
     
    async def get_ban(self, name_or_id):
        '''Prendre les bans d'un serveur'''
        guild = await self.client.fetch_guild(850043541610692608)
        for ban in await guild.bans():
            if name_or_id.isdigit():
                if ban.user.id == int(name_or_id):
                    return ban
            if str(ban.user).lower().startswith(name_or_id.lower()):
                return ban
    

    @commands.command()
    @commands.has_any_role(role["owner"], role["modo"], role["supermodo"])
    async def ping(self, ctx):
         """Renvoie la latence du bot"""

         latence = int(self.client.latency * 1000)
         embed1 = discord.Embed(title='PONG !', color=discord.Color.green(), description=f'La Latence de ce bot est de {int(self.client.latency *1000)}ms')
         embed2 = discord.Embed(title='PONG !', color=discord.Color.orange(), description=f'La Latence de ce bot est de {int(self.client.latency *1000)}ms')
         embed3 = discord.Embed(title='PONG !', color=discord.Color.red(), description=f'La Latence de ce bot est de {int(self.client.latency *1000)}ms')
         embed1.set_thumbnail(url='https://emoji.gg/assets/emoji/7431-the-connection-is-excellent.png')
         embed2.set_thumbnail(url='https://emoji.gg/assets/emoji/3657-the-connection-is-good.png')
         embed3.set_thumbnail(url='https://emoji.gg/assets/emoji/8920-the-connection-is-bad.png')
         if latence < 200:
             await ctx.send(embed=embed1)
         elif latence < 300 & latence < 200:
             await ctx.send(embed=embed2)
         elif latence > 300 :
             await ctx.send(embed=embed3)
    
    @commands.command(aliases=['effacer'])
    @commands.has_any_role(role["owner"], role["modo"], role["supermodo"])
    async def clear(self, ctx, nbr = None):
         """Suprimme les messages d'un salon"""
         await ctx.channel.purge(limit=int(nbr) + 1)
    
    @commands.command()
    @commands.has_any_role(role["owner"], role["modo"], role["supermodo"])
    async def accueil(self, ctx):
         """Envoie un message d'accueil"""
         await ctx.message.delete()
         channel = self.client.get_channel(850046027503632404)
         embed = discord.Embed(title=f"**Bienvenue au HUB NOCTURNE**", description=f"Bonjour et bienvenue sur le serveur, pour commencer, lis les règles du serveur ensuite rend toi dans le salon de rôles et choisis celui qui te correspond. Bonne Continuation sur Le Hub Nocturne.\n 💡 partage ce serveur avec tes ami(e)s : https://discord.gg/t9Y67asVbJ", color=discord.Color.teal())
         await channel.send(
             embed=embed,
             components = [
                 Button(style=ButtonStyle.URL,label= 'Notre site Web', url="https://discord.io/HubNocturne")
             ]
         )

    
    @commands.command(aliases=['dire','tell'])
    @commands.has_any_role(role["owner"], role["modo"], role["supermodo"])
    async def say(self, ctx,*text):
         """Répète le message demandé"""

         await ctx.message.delete()
         await ctx.send(" ".join(text))
    
    @commands.command()
    @commands.has_any_role(role["modo"], role["owner"], role["supermodo"])
    async def ban(self, ctx, member: discord.Member, *reason):
         """Bannie l'utilisateur choisie du serveur"""
         await ctx.message.delete()
         sanction_channel = ctx.guild.get_channel(861700222345412677)
         reason = " ".join(reason)
         await member.ban(reason=reason)
         embed = discord.Embed(title=f"Sanction", description=f'{member.mention} à été banni(e) pour la raison suivante :\n{reason}', color=discord.Color.teal())
         embed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
         await sanction_channel.send(embed=embed)
         userembed = discord.Embed(title=f"Sanction", description=f'{member.mention}, vous avez été banni(e) du Hub Nocturne car :\n{reason}', color=discord.Color.teal())
         userembed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
         await member.send(embed=userembed)
         
    
    @commands.command()
    @commands.has_any_role(role["modo"], role["owner"], role["supermodo"])
    async def kick(self, ctx, member: discord.Member, *reason):
         """Exclue l'utilisateur choisie du serveur"""

         sanction_channel = ctx.guild.get_channel(861700222345412677)
         await ctx.message.delete()
         reason = " ".join(reason)
         await member.kick(reason=reason)
         embed = discord.Embed(title=f"Sanction", description=f'{member.mention} à été explusé(e) pour la raison suivante :\n{reason}', color=discord.Color.teal())
         embed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
         await sanction_channel.send(embed=embed)
         userembed = discord.Embed(title=f"Sanction", description=f'{member.mention}, vous avez été expulsé(e) du Hub Nocturne car :\n{reason}', color=discord.Color.teal())
         userembed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
         await member.send(embed=userembed)
    
    @commands.command(pass_context=True)
    @commands.has_any_role(role['modo'],role['owner'],role['supermodo'])
    async def setgame(self, ctx, *, game : str):
         """Définit le jeu du bot"""
         await ctx.message.delete()
         member = ctx.message.author
         await ctx.message.delete()
         await self.client.change_presence(status=discord.Status.idle, activity=discord.Game(game))
     

    @commands.command()
    @commands.has_any_role(role['modo'],role['owner'],role['supermodo'])
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, name_or_id, *, reason=None):
        '''Débanni un membre du serveur'''

        sanction_channel = ctx.guild.get_channel(861700222345412677)
        await ctx.message.delete()
        ban = await self.get_ban(name_or_id)
        if not ban:
            return await ctx.send('Utilisateur introuvable !')
        await ctx.guild.unban(ban.user, reason=reason)
        embed = discord.Embed(title=f"Sanction", description=f'{ban.user.mention} à été débanni(e) du Hub Nocturne', color=discord.Color.teal())
        embed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
        await sanction_channel.send(embed=embed)
        userembed = discord.Embed(title=f"Sanction", description=f'{ban.user.mention}, vous avez été débanni du Hub Nocturne', color=discord.Color.teal())
        userembed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
        await ban.user.send(embed=userembed)
    
    @commands.command()
    @commands.has_any_role(role['modo'],role['supermodo'],role['owner']) 
    @commands.bot_has_permissions(manage_channels=True)
    async def mute(self, ctx, user: discord.Member, time: int=15, *reason):
        '''Rend muet un utilisateur du serveur'''
        schannel = ctx.guild.get_channel(861700222345412677)
        secs = time * 60
        reason = " ".join(reason)
        await ctx.message.delete()
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=False)
        embed = discord.Embed(title=f"Sanction", description=f'{user.mention} est muet(te) pendant {time} min(s), pour la raison suivante:\n{reason}', color=discord.Color.teal())
        embed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
        userembed = discord.Embed(title=f"Sanction", description=f'{user.mention}, vous êtes muet(te) pendant {time} min(s), pour la raison suivante:\n{reason}', color=discord.Color.teal())
        userembed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
        await schannel.send(embed=embed)
        await user.send(embed=userembed)
        await asyncio.sleep(secs)
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        uembed = discord.Embed(title=f"Sanction", description=f'{user.mention} n\'est plus muet(te).', color=discord.Color.teal())
        uembed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
        userembed = discord.Embed(title=f"Sanction", description=f'{user.mention} vous n\'êtes plus muet(te).', color=discord.Color.teal())
        userembed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
        await schannel.send(embed=uembed)
        await user.send(embed=userembed)

    @commands.command()
    @commands.has_any_role(role['modo'],role['supermodo'],role['owner'])
    @commands.bot_has_permissions(manage_channels=True)
    async def unmute(self, ctx, user: discord.Member):
        await ctx.message.delete()
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        uembed = discord.Embed(title=f"Sanction", description=f'{user.mention} n\'est plus muet(te).', color=discord.Color.teal())
        uembed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
        schannel = ctx.guild.get_channel(861700222345412677)
        await schannel.send(embed=uembed)
        userembed = discord.Embed(title=f"Sanction", description=f'{user.mention} vous n\'êtes plus muet(te).', color=discord.Color.teal())
        userembed.set_thumbnail(url='https://emoji.gg/assets/emoji/7609-admin.png')
        await user.send(embed=userembed)
 

    @commands.command()
    @commands.has_any_role(role['supermodo'], role['owner'])
    async def recrute(self, ctx, user : discord.Member, *job):
        job = " ".join(job)
        modo = discord.utils.get(user.guild.roles, name='🚫 MOD')
        admin = discord.utils.get(user.guild.roles, name='🚨 Super MOD')
        if job == 'modérateur' :
            if admin in user.roles:
                await user.remove_roles(admin)
            await user.add_roles(modo)
            await ctx.send(f'Bib Boub Bib ...{user.mention} est promu(e) modérateur !')
        elif job == 'administrateur':
            if modo in user.roles:
                await user.remove_roles(modo)
            await user.add_roles(admin)
            await ctx.send(f'Bib Boub Bib ... , {user.mention} est promu(e) administrateur !')
        else :
            await ctx.send(f'Bib Boub Bib ... , {job} n\'est pas un job disponible sur notre serveur !')
    
    @commands.command()
    @commands.has_any_role(role['supermodo'], role['owner'])
    async def downgrade(self, ctx, user : discord.Member):
     modo = discord.utils.get(user.guild.roles, name='🚫 MOD')
     admin = discord.utils.get(user.guild.roles, name='🚨 Super MOD')
     if modo in user.roles:
         await user.remove_roles(modo)
     elif admin in user.roles:
         await user.remove_roles(admin)
     else :
         await ctx.send('Cette utilisateur ne peux pas être rétrograder car il est seulement Membre du serveur.')
