import os
import discord
import datetime
import json
import io
import traceback
import time
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

with open('./setting/config.json', 'r') as cjson:
    config = json.load(cjson)

with open('./setting/role.json', 'r') as cjson:
    role = json.load(cjson)

def setup(client):
     client.add_cog(info(client))

class info(commands.Cog):

    def __init__(self, client):
         self.client = client
    
    @commands.command(aliases=['sf', 'serveurinformation'])
    async def serverinfo(self, ctx):
     time = ctx.guild.created_at
     embed = discord.Embed(title=f"__Information sur le {ctx.guild.name}__", color=discord.Color.dark_theme())
     embed.add_field(name="Créé le :", value=time.strftime('%d/%m/%Y'), inline=False)
     embed.add_field(name="Fondateur :", value=f"{ctx.guild.owner}",inline=False)
     embed.add_field(name="Région :", value=f"{ctx.guild.region}",inline=False)
     embed.add_field(name="ID :", value=f"{ctx.guild.id}",inline=False)
     embed.set_thumbnail(url=f"{ctx.guild.icon_url}")

     await ctx.send(embed=embed)
    
    @commands.command(aliases=['ui', 'user'])
    async def userinfo(self, ctx, user: discord.Member = None):
         '''Renvoie, dans un embed, les informations d'un utilisateur choisi'''
         user = user or ctx.message.author
         guild = ctx.message.guild
         guild_owner = guild.owner
         avi = user.avatar_url
         roles = sorted(user.roles, key=lambda r: r.position)
         status = user.status
         rolenames = ', '.join([r.name for r in roles if r != '@everyone']) or 'None'
         time = ctx.message.created_at
         if status == discord.Status.online:
             desc = f'{user.name} est connecté(e)'
             em = discord.Embed(timestamp=time)
             em.color = discord.Color.dark_theme()
             em.set_author(name=desc, icon_url='https://emoji.gg/assets/emoji/5519-online.png')
             em.add_field(name='Pseudo :', value=user.name, inline=False),
             em.add_field(name='Compte crée le :', value=user.created_at.__format__('%d/%m/%Y'),inline=False),
             em.add_field(name='à rejoin le :', value=user.joined_at.__format__('%d/%m/%Y'),inline=False),
             em.add_field(name='Rôle(s) :', value=rolenames, inline=False)
             em.set_thumbnail(url=avi or None)
             await ctx.send(embed=em)
         elif status == discord.Status.dnd:
             desc = f'{user.name} est occupé(e)'
             em = discord.Embed(timestamp=time)
             em.color = discord.Color.dark_theme()
             em.set_author(name=desc, icon_url='https://emoji.gg/assets/emoji/2612-dnd.png')             
             em.add_field(name='Pseudo :', value=user.name, inline=False),
             em.add_field(name='Compte crée le :', value=user.created_at.__format__('%d/%m/%Y'),inline=False),
             em.add_field(name='à rejoin le :', value=user.joined_at.__format__('%d/%m/%Y'),inline=False),
             em.add_field(name='Rôle(s) :', value=rolenames, inline=False)
             em.set_thumbnail(url=avi or None)
             await ctx.send(embed=em)
         elif status == discord.Status.offline:
             desc = f'{user.name} est déconnecté(e)'
             em = discord.Embed(timestamp=time)
             em.color = discord.Color.dark_theme()
             em.set_author(name=desc, icon_url='https://emoji.gg/assets/emoji/7783-offline.png')
             em.add_field(name='Pseudo :', value=user.name, inline=False),
             em.add_field(name='Compte crée le :', value=user.created_at.__format__('%d/%m/%Y'),inline=False),
             em.add_field(name='à rejoin le :', value=user.joined_at.__format__('%d/%m/%Y'),inline=False),
             em.add_field(name='Rôle(s) :', value=rolenames, inline=False)
             em.set_thumbnail(url=avi or None)
             await ctx.send(embed=em)
         else :
             desc = f'{user.name} est inactif'
             em = discord.Embed(timestamp=time)
             em.color = discord.Color.dark_theme()
             em.set_author(name=desc, icon_url='https://emoji.gg/assets/emoji/6868-idle.png')
             em.add_field(name='Pseudo :', value=user.name, inline=False),
             em.add_field(name='Compte crée le :', value=user.created_at.__format__('%d/%m/%Y'),inline=False),
             em.add_field(name='à rejoin le :', value=user.joined_at.__format__('%d/%m/%Y'),inline=False),
             em.add_field(name='Rôle(s) :', value=rolenames, inline=False)
             em.set_thumbnail(url=avi or None)
             await ctx.send(embed=em)
         
    @commands.command(aliases=['role'])                            
    async def roleinfo(self, ctx, *, rolename):
        '''Enviue des informations sur un rôle du serveur'''
        try:
            role = discord.utils.get(ctx.message.guild.roles, name=rolename)
        except:
            return await ctx.send(f"Role could not be found. The system IS case sensitive!")

        em = discord.Embed(description=f'Role ID: {str(role.id)}', color=role.color or discord.Color.green())
        em.title = role.name
        perms = ""
        if role.permissions.administrator:
            perms += "Administrateur, "
        if role.permissions.create_instant_invite:
            perms += "Créer une invitation, "
        if role.permissions.kick_members:
            perms += "Expulser des membres, "
        if role.permissions.ban_members:
            perms += "Bannir des Membres, "
        if role.permissions.manage_channels:
            perms += "Gérer les salons, "
        if role.permissions.manage_guild:
            perms += "Gérer le serveur, "
        if role.permissions.add_reactions:
            perms += "Ajouter des réaction, "
        if role.permissions.view_audit_log:
            perms += "Voir les logs du serveur, "
        if role.permissions.read_messages:
            perms += "Lire les messages, "
        if role.permissions.send_messages:
            perms += "Envoyer des messages, "
        if role.permissions.send_tts_messages:
            perms += "Envoyer des messages de synthèse vocale, "
        if role.permissions.manage_messages:
            perms += "Gérer les messages, "
        if role.permissions.embed_links:
            perms += "Attacher des liens, "
        if role.permissions.attach_files:
            perms += "Envoyer des fichiers, "
        if role.permissions.read_message_history:
            perms += "Voir les anciens messages, "
        if role.permissions.mention_everyone:
            perms += "Mentionner tout le monde et les autres rôles, "
        if role.permissions.external_emojis:
            perms += "Utiliser des émojis externe, "
        if role.permissions.connect:
            perms += "Se connecter, "
        if role.permissions.speak:
            perms += "Parler, "
        if role.permissions.mute_members:
            perms += "Couper le micro des membres, "
        if role.permissions.deafen_members:
            perms += "Mettre en sourdine des membres, "
        if role.permissions.move_members:
            perms += "Déplacer des membres, "
        if role.permissions.use_voice_activation:
            perms += "Utiliser appuyer pour parler, "
        if role.permissions.change_nickname:
            perms += "Peut changer de pseudo, "
        if role.permissions.manage_nicknames:
            perms += "Gère les surnoms, "
        if role.permissions.manage_roles:
            perms += "Gère les rôles, "
        if role.permissions.manage_webhooks:
            perms += "Gère les integrations, "
        if role.permissions.manage_emojis:
            perms += "Gère les émojis, "

        if perms is None:
            perms = "None"
        else:
            perms = perms.strip(", ")

        roleh = role.hoist

        if roleh == True :
           roler = 'Oui'
        else :
           roler = 'Non'
        
        rolem = role.managed
        
        if rolem == True:
            rolemr = 'Oui'
        else:
            rolemr = 'Non'

        rolemen = role.mentionable
        if rolemen == True:
            rolemenr = 'Oui'
        else :
            rolemenr = 'Non'

        em.add_field(name='Visible', value=str(roler), inline=False)
        em.add_field(name='Position dans la list', value=str(role.position), inline=False)
        em.add_field(name='Géré par une integration', value=str(rolemr), inline=False)
        em.add_field(name='Mentionable', value=str(rolemenr), inline=False)
        em.add_field(name='Membre possèdent le rôle', value=str(len(role.members)), inline=False)

        pages = []
        pages.append(em)

        em2 = discord.Embed(description=f'Role ID: {str(role.id)}', color=role.color or discord.Color.green())
        em2.title = role.name
        em2.add_field(name='Permissions', value=perms, inline=False)

        pages.append(em2)

        thing = str(role.created_at.__format__('%d/%m/%Y'))

        p_session = PaginatorSession(ctx, footer=f'Crée le: {thing}', pages=pages)
        await p_session.run()

        