import discord
from discord.ext import commands
from discord.ext.commands import Bot
import re
from collections import namedtuple, deque
from traceback import print_exc
from typing import Dict
from urllib import parse as url_parse
from urllib import parse
from contextlib import redirect_stdout
import platform
import psutil
import string 
import giphypop
import asyncio
import random
import time
import sys
import json
import os
import io
import os.path
import urllib.request
import discord.abc
import aiohttp
import stat
import time
import subprocess
import traceback
import datetime
import praw
import inspect
import textwrap
import weebhooks
from motor.motor_asyncio import AsyncIOMotorClient
from googlesearch import search
import disputils #Some utils
import threading
from context import CustomContext

prefix = "b-"

def randomColor():
    clist = ['blue', 'blurple', 'dark_blue', 'dark_gold', 'dark_green', 'dark_grey', 'dark_magenta', 'dark_orange', 'dark_purple', 'dark_red', 'dark_teal', 'darker_grey', 'gold', 'green', 'greyple', 'light_grey', 'lighter_grey', 'magenta', 'orange', 'purple', 'red', 'teal']
    return eval(f"discord.Color.{random.choice(clist)}()")



with open('info.json') as f:
    config = json.load(f)
    botowner = 478675118332051466


with open('tokens.json') as f: # Could use envs, but hopefully someone might land up PRing that.
    tokens = json.load(f)
    




reddit = praw.Reddit(
    client_id=tokens["reddit"]["id"],
    client_secret=tokens["reddit"]["secret"],
    user_agent='Ditto Meme'                 
) 

db = AsyncIOMotorClient(tokens["db"],retryWrites=False).thekirbybotdb

e6login = tokens["e621"]
uaheader = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}



async def getprefix(bot,message):
    pre = None
    if isinstance(message.channel, discord.DMChannel): return '--'
    x = await db.prefixes.find_one({ "id": str(message.guild.id) })
    try:
        if bot.user.id == 538765900841746444:
            pre = "b-"
        else:
            pre = x['prefix']
    except:
        pre = ['--',f"<@{bot.user.id}> ",f"<@{bot.user.id}>"]
    return pre




bot = discord.ext.commands.AutoShardedBot(command_prefix=getprefix, description='A general bot for memes and moderation', pm_help=False, fetch_offline_members=True,  activity=discord.Game(name="Starting the bot..."), status=discord.Status("dnd"))

bot.remove_command('help')
GIPHY_TOKEN = tokens["giphy"]


    



async def status_task():
  p = ("--" if bot.user.id == 508268149561360404 else "b-")
  games = [
    "with a cookie",
    "with memes",
    "with some speed",
    "with a banana",
    "with an apple",
    "with a cake",
    "with a potato",
    "with a Maximum Tomato",
    f"with {str(len(bot.users))} users",
    f"with {str(len(bot.guilds))} servers",
    f"with {str(len(bot.commands))} commands",
    "with a torch",
    "with a Waddle Dee",
    "with the devs",
    "with Discord's API",
    "with other bots",
    "with another language",
    "with a keyboard",
    "with the banland",
    "with brackets and quotes",
    "Kirby's Nightmare in Dreamland",
    "with an interdimensional traveller",
    "with Python and Javascript",
    "with about 2000 lines of code",
    "with the developer's mental sanity",
    "with broken code",
    "with actual working code",
    "with the dev's lives",
    "with another bot", 
    "with a foo bar",
    "with a greeting to the world",
    "with some Pokemon",
    "with Wumpus"
  ]
  while True:
   ping_lvl = round(bot.latency * 1000)
   if not ping_lvl > 200:
    await bot.change_presence(activity=discord.Game(name=f"{random.choice(games)} || Type {p}help for commands"))
   else:
    await bot.change_presence(activity=discord.Game(name=f"Bot affected by Discord issues."),status=discord.Status.idle)
   
   await asyncio.sleep(20)


nouns = open("list/nouns.txt","r").read().splitlines()
adjectives = open("list/adjectives.txt","r").read().splitlines()
verbs = open("list/verbs.txt","r").read().splitlines()


bot.starttime = 0





@bot.event
async def on_ready(): 
    bot.starttime = time.time()
    bot.db = db
    bot.commands_run = 0
    bot.session = aiohttp.ClientSession()
    await bot.change_presence(status=discord.Status("online"))
    bot.loop.create_task(status_task())
    print("++++++++++++++++++")
    print("Succesfully logged in as: " + str(bot.user.name))
    print("With an ID of: " + str(bot.user.id))
    print("At: " + time.asctime( time.localtime(time.time()) ))
    print("Members in total: " + str(len(bot.users)))
    print("Servers in total: " + str(len(bot.guilds)))
    print("++++++++++++++++++")
    #bot.load_extension("music")
    
    if bot.user.id == 508268149561360404:
        bot.load_extension('dbl')
        bot.load_extension('ddb')

    # if os.path.exists("restart.txt"):
    #     fl = open("restart.txt")
    #     ids = fl.readlines()
    #     channel = await bot.get_channel(ids[0])
    #     await channel.fetch_message(ids[1]).edit("Successfully restarted!")
    #     fl.close()
    #     os.remove("restart.txt")







#          #
#          #
# Commands #
#          #
#          #




@bot.command(brief="The changelog.",description="Displays everything that has been changed recently.")
async def changelog(ctx):
    # changelog = open("changelog.txt",'r')
    # Truechangelog = changelog.read()
    # await ctx.send(Truechangelog)
    # changelog.close()
    #Time for the new code ;3

    announcements = bot.get_channel(623553307964604417)
    message_list = await announcements.history(limit=10).flatten()
    last_message = None
    for x in message_list:
        if x.author.id == 478675118332051466:
            last_message = x
            break
    
    em = discord.Embed(title="Latest Changelog (announcement)",description=str(last_message.content),color=discord.Color.magenta())
    em.set_author(name=last_message.author.name,icon_url=last_message.author.avatar_url)
    dt_format = last_message.created_at.strftime("%A %d %B %Y (%H:%M.%S)")
    em.set_footer(text=f"Sent at {dt_format}")
    await ctx.send(embed=em)


@bot.command(brief="The Support Server!",description="Sends an invite link to the bot's server.")
async def botserver(ctx):
    await ctx.send(ctx.message.author.mention + " here you go: " + "https://discord.gg/dcBumZJ")


@bot.command(pass_context=True,brief="Invite the bot to your server!",description="Gives you an invite link to invite the bot to your server.")
async def invite(ctx):
    embed=discord.Embed(title="Invite me to your server", url=f"https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&permissions=204811351&scope=bot", color=0x7289da)
    embed.set_author(name="The Kirby Bot",icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)
 
 
@bot.command(brief="Go to the bot's Patreon.",description="Sends a Patreon link in chat to donate to the bot and help the bot.",aliases=["patreon"])
async def donate(ctx):
    await ctx.send("Click here to donate to the bot: https://www.patreon.com/mainuserdrive")
	

@bot.command(brief="Grabs info on a github repo")
async def github(ctx, repo : str):
    buff = await bot.session.get(f"https://api.github.com/search/repositories?q={repo}")
    json = await buff.json()
    if json["total_count"] == 0:
        return await ctx.send("No repos found")
    repo = json["items"][0]
    em = discord.Embed(title=repo["full_name"],description=repo['description'],color=discord.Color.green())
    em.add_field(name="Watchers",value=f"{repo['watchers_count']} watchers")
    em.add_field(name="Fork Count",value=f"{repo['forks_count']} forkers")
    em.add_field(name="Language",value=f"{repo['language']}")
    em.add_field(name="License",value=f"{repo['license']['name']}")
    em.set_footer(text="Would add more, but Git's API doesn't have that much.")

    await ctx.send(embed=em)


@bot.command(brief="Gets a bunch of bot info, since why not")
async def stats(ctx):
    msg = await ctx.send("Getting info... Please wait")
    second = round((time.time() - bot.starttime))
    minute = round(second / 60)
    hour = round(minute / 60)
    day = round(hour / 24)

    hidden = 0
    canrun = 0
    nsfw = 0
    for command in bot.commands:
        if command.hidden:
            hidden = hidden + 1
        try:
            if await command.can_run(ctx):
                canrun = canrun + 1
        except discord.ext.commands.CommandError:
            for ch in command.checks:
                if "is_nsfw" in str(ch):
                    nsfw = nsfw + 1
            else:
                pass
        except Error as e:
            raise e

    usernames = []
    for x in config["SpecialThanks"]:
        user = await bot.fetch_user(x)
        usernames.append(user.name)

    usernames = "\n".join(usernames)
    em = discord.Embed(title="Bot Stats",color=0xb50db9)
    em.set_author(name=bot.user.name,icon_url=bot.user.avatar_url,url="https://thekirbybot.xyz")
    em.add_field(name="Special Thanks",value=f"{usernames}")
    em.add_field(name="Uptime",value=f"{day} days, {hour % 24} hours, {minute % 60} minutes, {second % 60} seconds",inline=True)
    em.add_field(name="User Count",value=f"{len(bot.users)}",inline=True)
    em.add_field(name="Server Count",value=f"{len(bot.guilds)}",inline=True)
    em.add_field(name="Commands Run",value=f"{bot.commands_run}",inline=True)
    em.add_field(name="Command Count",value=f"{len(bot.commands)} commands in total \n{hidden} admin commands\n{nsfw} NSFW commands hidden\n{len(bot.commands) - canrun - nsfw} commands unable to run (No Permissions)",inline=False)
    #Lil var switch here#
    second = round((time.time() - psutil.boot_time()))
    minute = round(second / 60)
    hour = round(minute / 60)
    day = round(hour / 24)
    
    em.add_field(name="Being Hosting On",value=f"OS: {platform.system()} {platform.release()}\nSystem Uptime: {day} days, {hour % 24} hours, {minute % 60} minutes, {second % 60} seconds",inline=False)
    em.add_field(name="Version Lists",value=f"Python Version: {str(platform.python_version())}\nDiscord.py Version: {discord.__version__}")
    ramav = psutil._common.bytes2human(psutil.virtual_memory().available)
    ramused = psutil._common.bytes2human(psutil.virtual_memory().used)
    em.add_field(name="System Stats",value=f"**--System Wide--**\nCPU Usage: {psutil.cpu_percent()}%\nRAM Available: {ramav}B\nRAM Used: {ramused}B")
    em.set_footer(text=f"Bot made with <3 by {discord.utils.get(bot.users,id=478675118332051466)}",icon_url=discord.utils.get(bot.users,id=478675118332051466).avatar_url)
    
    await msg.edit(content=None,embed=em)


@commands.has_permissions(manage_roles = True)
@bot.command(brief="Adds or removes a role from a user, or yourself")
async def role(ctx, user : discord.Member,*,role : discord.Role):
    if ctx.author.top_role.position <= user.top_role.position:
        return await ctx.send("That person has a higher role than you, so no.")
    if role.id in [x.id for x in user.roles]:
        await user.remove_roles(role)
        await ctx.send(f"Removed **{role.name}** from **{user.display_name}**")
    else:
        await user.add_roles(role)
        await ctx.send(f"Added **{role.name}** to **{user.display_name}**")


@commands.cooldown(1, 30, commands.BucketType.default)	
@commands.has_permissions(manage_messages = True)
@bot.command(brief="Cleans an amount of messages (limit 1000) (might lag, do not start another purge while one is in progress)")
async def purge(ctx, number : int = 5,bulk = True):
    if number > 1000: return await ctx.send("No, I can not purge more than 1000 messages")
    def check(m):
        return True

    if number <= 100:
        await ctx.message.delete()
        dele = await ctx.message.channel.purge(limit=number,check=check,bulk=bulk)
        return await ctx.send(f"{discord.utils.get(bot.emojis,id=561904367201157121)} Deleted {len(dele)} messages")

    deleted = 0
    while not number == 0:
        if number > 100:
            com = await ctx.message.channel.purge(limit=100,check=check,bulk=bulk)
            deleted = deleted + len(com)
            number = number - 100
        else:
            com = await ctx.message.channel.purge(limit=number,check=check,bulk=bulk)
            deleted = deleted + len(com)
            number = number - number
        time.sleep(0.1)

    await ctx.send(f"{discord.utils.get(bot.emojis,id=561904367201157121)} Deleted {deleted} messages")


@commands.has_permissions(ban_members = True)
@bot.command(brief="Unbans a user from the server",description="(THE COMMAND REQUIRES A PING TO UNBAN (DO THIS BY <@(id)> REPLACING (id) WITH THE USER'S ID))")
async def unban(ctx, user : discord.User,reason : str = "No Reason Provided"):
    try:
        await ctx.guild.unban(user=user,reason=f"{ctx.author} - {reason}")
        await ctx.send(f"Successfully unbanned {user}... They was un-spartan kicked")
    except:
        await ctx.send("No Ban Found")
  


@commands.guild_only()
@commands.has_permissions(manage_guild = True)
@bot.command(brief="Sets the prefix in the server")
async def prefix(ctx,*,prefix : str):
    bot.db.prefixes.update_one({"id": str(ctx.guild.id)}, {"$set": {"prefix": prefix}}, upsert=True)
    await ctx.send(f"The prefix was set to ``{prefix}`` successfully!")
    x = await bot.db.modlog.find_one({ "id": ctx.guild.id })
    if x:
        chnl = bot.get_channel(int(x["channel"]))
        if chnl:
            em = discord.Embed(title="Prefix Change",color=discord.Color.dark_gold())
            em.add_field(name="By",value=ctx.author)
            em.add_field(name="New Prefix",value=prefix,inline=False)
            await chnl.send(embed=em)



@commands.guild_only()
@commands.has_permissions(manage_guild = True)
@bot.command(brief="Sets the welcome channel for this guild (See --help welcome for format)",description=f"Format:\n" + "{usr} - New Member's Name")
async def welcome(ctx, channel : discord.TextChannel,*, message):
    bot.db.welc.update_one({"id": str(ctx.guild.id)}, {"$set": {"message": message, "channel": str(channel.id)}}, upsert=True)
    await ctx.send(f"Successfuly changed welcome message to: ``{message}``")

 
@commands.guild_only()
@commands.has_permissions(manage_guild = True)
@bot.command(brief="Sets the leaving channel for this guild (See --help leave for format)",description=f"Format:\n" + "{usr} - New Member's Name")
async def leave(ctx, channel : discord.TextChannel,*, message):
    bot.db.leave.update_one({"id": str(ctx.guild.id)}, {"$set": {"message": message, "channel": str(channel.id)}}, upsert=True)
    await ctx.send(f"Successfuly changed leaving message to: ``{message}``")



@commands.guild_only()
@commands.has_permissions(manage_guild=True) 
@bot.command(brief="Enables raidmode for the server (See --help raidmode)", description="you do this")
async def raidmode(ctx, option = None):
    if option.lower() == "on": 
        bot.db.raidmode.update_one({"id": str(ctx.guild.id)}, {"$set": {"status": True}}, upsert=True)
        return await ctx.send("Raidmode has been enabled. Any users that attempt to join will be kicked.")
    elif option.lower() == "off":
        bot.db.raidmode.delete_one({"id": str(ctx.guild.id)}) 
        return await ctx.send("Raidmode has been disabled. Users can join now.")
    else:
        return await ctx.send("Please enter an option: on/off.")



@commands.guild_only()
@bot.command(brief="Shows more info about a certain user",aliases=["ui","u"])
async def userinfo(ctx, user : discord.Member = "plcholder"):
    if user == "plcholder":
        user = ctx.message.author
    emojis = []
    #Determine the badges
    if user.id in config["Admin"]:
        emojis.append(str(discord.utils.get(bot.emojis,id=561904367528312862)))
    #Now, the Embed
    em = discord.Embed(title=f"User info for {user} {''.join(emojis)}",color=discord.Color.teal())
    em.add_field(name="Username",value=str(user.name),inline=True)
    em.add_field(name="Discriminator",value=f"#{user.discriminator}",inline=True)
    em.add_field(name="ID",value=str(user.id))
    if user.nick:
        em.add_field(name="Nickname",value=str(user.nick))
    #Code to determine what platform
    pltfrm = "working"
    if str(user.mobile_status) != "offline":
        pltfrm = "Mobile"
    elif str(user.web_status) != "offline":
        pltfrm = "Website"
    elif str(user.desktop_status) != "offline":
        pltfrm = "Computer"
    else:
        pltfrm = "placeholder"
    #End of determination
    em.add_field(name="Status",value=(f"{pltfrm} ({str(user.status).capitalize()})" if pltfrm != "placeholder" else "Offline everywhere"))
    
    if isinstance(user.activity,discord.Spotify):
        title = "Playing on Spotify"
        gm = f"Song: {user.activity.title}\nBy: {', '.join(user.activity.artists)}\nAlbum: {user.activity.album}"
    elif isinstance(user.activity,discord.Streaming):
        title = "Streaming"
        gm = f"{user.activity.name}"
    elif isinstance(user.activity,discord.Game) or isinstance(user.activity,discord.Activity):
        title = "Playing"
        gm = f"{user.activity.name}"
    else:
        title = "Playing"
        gm = "Not playing anything."

    em.add_field(name=title,value=gm)
    em.add_field(name="A bot", value=("Yes" if user.bot else "No"))
    #Checking if the user has a joined_at attribute
    if user.joined_at:
        formatted = user.joined_at.strftime("%A %d %B %Y (%H:%M.%S)")
        em.add_field(name="Joined the server at",value=formatted)
    #Formatting of created_at
    fm = user.created_at.strftime("%A %d %B %Y (%H:%M.%S)")

    em.add_field(name="Joined Discord at",value=fm)
    em.set_footer(text="Userinfo redesign is in beta")
    em.set_thumbnail(url=user.avatar_url_as(size=1024))

    await ctx.send(embed=em)
    

 
@bot.command(brief="Randomly selects the top 20 Reddit submissions on the memes subreddit")
async def meme(ctx):
    async with ctx.message.channel.typing():
        memes_submissions = reddit.subreddit('memes').hot()
        post_to_pick = random.randint(1, 20)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)

        embed=discord.Embed(title=submission.title,color=0xb50db9)
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"URL: {submission.url}")
        await ctx.send(embed=embed)

 
@bot.command(pass_context=True, brief="DAY BE STEALING MAH BUCKET",aliases=['ohnoes'],description="Sends a bucket meme in chat.")
async def bucket(ctx):
  file = discord.File("memes/bucket.jpg", "bucket.jpeg")
  await ctx.send(file=file)
  

@bot.command(brief="Makes👏spaces👏into👏clapping👏emojis👏because👏why👏not",aliases=['memereview'])
async def clap(ctx,*,text):
    table = text.split(' ') 
    em = discord.Embed(title="👏ify")
    em.add_field(name="Original Text",value=f"``{text}``")
    em.add_field(name="New Text", value=f"``👏{'👏'.join(table)}👏``")
    await ctx.send(embed=em)

@bot.command(brief="Sets your AFK status")
async def afk(ctx,*,status : str):
    await bot.db.afk.update_one({"id": ctx.author.id}, {"$set": {"status": status}}, upsert=True)
    await ctx.send(f"Alright! You are now AFK for ``{status}``.")

@bot.command(brief="Noot Noot!",aliases=['pingu'],description="Sends a random Noot Noot meme in chat.")
async def nootnoot(ctx):
    file = discord.File("memes/pingu/nootnoot" + str(random.randint(1,4)) + ".jpg", "pingu.jpeg")
    await ctx.send(file=file)

 
@bot.command(brief="Sends a suggestion to the devs")
async def suggestion(ctx, *, text : str):
    svr = bot.get_guild(508305433711083520)
    chnl = svr.get_channel(540797383353696266)
    suggestionhook.send(f"**Suggestion Recieved**\n``{text}``\nUser: {ctx.author}")
    await ctx.send("**Sent the suggestion to the devs!**")

@commands.has_permissions(kick_members = True)
@bot.command(pass_context=True,brief="Kicks a user",description="Kicks a user from your server. The user will be able to rejoin with a new invite link.")
async def kick(ctx, user : discord.Member):
    await ctx.guild.kick(user)
    choices [
        f"**{user.name}** flew off the stage but forgot to recover",
        f"**{user.name}** got shown the door",
        f"**{user.name}** got their membership permissions revoked",
        f"**{user.name}** got oof'd",
        f"**{user.name}** got 307'd"
    ]
    await ctx.send(content=random.choice(choices))

@commands.has_permissions(ban_members = True)
@bot.command(pass_context=True,brief="Bans a user",description="Permanently bans a user from your server. Optionally, add the reason at the end of the message")
async def ban(ctx, user : discord.Member,*, reason: str):
    await ctx.guild.ban(user,reason=f"Banned by {ctx.author}: {reason}")
    choices = [
        f"**{user.name}** flew and bit the dust",
        f"**{user.name}** found a wild 404 error, and trusted it.",
        f"**{user.name}** got game ended",
        f"**{user.name}** saw stars and fainted",
        f"**{user.name}** was forced to say bye-bye",
        f"**{user.name}** decided to see the wrong end of the hammer.",
        f"**{user.name}** got Ctrl + Alt + Yeeted (im sorry programmers)",
        f"**{user.name}** struck an angry chicken"
    ]
    await ctx.send(content=random.choice(choices))


@commands.has_permissions(ban_members = True)
@bot.command(pass_context=True,brief="Bans a user not in your server",description="Permanently bans a user from your server. Optionally, add the reason at the end of the message")
async def hackban(ctx, user, *, reason: str = "No Reason Provided"):
    user_object = discord.Object(int(user))
    user_info = await bot.fetch_user(user)
    await ctx.guild.ban(user_object,reason=f"Hackbanned by {ctx.author}: {reason}")
    await ctx.send(content=f"{str(user_info)} got banned like magic.")


@commands.has_permissions(manage_nicknames = True)
@bot.command(brief="Scans through the members and dehoists them",description="Scans through the members and checks if they have a non-alphabetical character at the start of their nick. If they do, change their nickname.")
async def dehoist(ctx,*, newnick : str = "hoister no hoisting"):
    pattern = re.compile('\W')
    
    if not ctx.guild.me.permissions_in(ctx.channel).manage_nicknames:
        return await ctx.send("I can not run that because I do not have the Manage Nicknames permission")

    count = 0
    mlist = []
    msg = await ctx.send(f"Alright! Scanning and changing nicknames{bot.get_emoji(528578022748454944)}")
    for x in ctx.guild.members:
        if re.sub(pattern, '', x.display_name[0]) == "":
            try:
                pnick = x.display_name
                await x.edit(nick=newnick,reason=f"Dehoist Command (Ran by {ctx.author})")
                count = count + 1
                mlist.append(f"{count}. {x} // {pnick}")
                await msg.edit(content=f"Edited {count} nicknames so far. {bot.get_emoji(528578022748454944)}")
            except discord.Forbidden:
                await ctx.send(f"Failed to change nick of {x} due to lack of permissions..")
            except Exception as e:
                raise e
    
    if count is not 0:
        st = "\n".join(mlist)
        x = await bot.session.post("https://hasteb.in/documents",data=f'Format: (username) // (old nickname)\n\n{st}')
        buff = await x.json()
        await msg.edit(content=f"Changed **{count}** nicknames.\nList: https://hasteb.in/{buff['key']}")
    else:
        await msg.edit(content=f"No nicknames found. No changes made.")


@bot.command(brief="Gets an Emoji's Information (Must be a custom emoji)",description="Gets information from a custom Discord emoji.")
async def emojiinfo(ctx, emoji : discord.Emoji):
    embed=discord.Embed(title="", description="", color=0xb50db9)
    embed.set_author(name="The Kirby Bot",icon_url=bot.user.avatar_url)
    embed.set_thumbnail(url=emoji.url)
    embed.add_field(name="Name", value=emoji.name, inline=True)
    embed.add_field(name="ID", value=emoji.id, inline=True)
    embed.add_field(name="Require Colons?", value=str(emoji.require_colons), inline=True)
    embed.add_field(name="Twitch Managed?", value=str(emoji.managed), inline=True)
    embed.add_field(name="Server", value=str(emoji.guild.name), inline=True)
    embed.add_field(name="Created At", value=str(emoji.created_at), inline=True)
    await ctx.send(embed=embed)   
  



@commands.cooldown(1, 30, commands.BucketType.default)		
@bot.command(pass_context=True,brief="Send a message to the bot developers about the bot",description="Sends a message to the bot developers about the bot")
async def devmsg(ctx, *, msg):
    await ctx.send("**Succesfully sent your message to the devs:white_check_mark:**")
    chnl = bot.get_channel(558699099331756043)
    embed=discord.Embed(title="**Developer Message**", description=msg, color=0xb50db9)
    embed.add_field(name="Sent By", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=False)
    embed.add_field(name="Server:", value=ctx.message.guild.name, inline=False)
    embed.set_footer(text=f"Time Sent: {time.asctime(time.localtime(time.time()))}")
    await chnl.send(embed=embed)
  
  
@commands.cooldown(1,10,commands.BucketType.default)
@bot.command(brief="Retrieves the time the bot can communicate with Discord")
async def ping(ctx):
    edittime = time.time()
    pingtime = round(bot.latency * 1000,2)
    nekoslife = "Retrieving nekos.life response time.."
    furrybot = "Retrieving furry.bot response time.."
    msg = await ctx.send("Pinging in the 90s, its a new place you want to be!")

    embed=discord.Embed(title="", url="", description="",color=randomColor())
    embed.set_author(name=bot.user.name,icon_url=bot.user.avatar_url)
    embed.add_field(name="Ping!", value=f"{pingtime}ms Latency\nRetrieving edit time...\n{nekoslife}\n{furrybot}", inline=False)
    await msg.edit(content=None,embed=embed)

    edittime = round((time.time() - edittime) * 100,2)
    embed.set_field_at(index=0,name="Ping!",value = f"{pingtime}ms Latency\n{edittime}ms Edit Latency\n{nekoslife}\n{furrybot}")
    await msg.edit(content=None,embed=embed)

    #Getting nekos.life response time#
    try:
        nekoslife = time.time()
        buff = await bot.session.get("https://nekos.life/api/v2/img/bj")
        json = await buff.json()
        nekoslife = f"{round((time.time() - nekoslife) * 100,2)}ms Response time (nekos.life)"
    except Exception as e:
        nekoslife = "Unable to get nekos.life response time."

    embed.set_field_at(index=0,name="Ping!",value = f"{pingtime}ms Latency\n{edittime}ms Edit Latency\n{nekoslife}\n{furrybot}")
    await msg.edit(content=None,embed=embed)

    #Getting furry.bot response time#
    try:
        furrybot = time.time()
        buff = await bot.session.get("https://api.furry.bot/furry/nsfw/yiff/gay") #Use an NSFW endpoint for the memes
        json = await buff.json()
        furrybot = f"{round((time.time() - furrybot) * 100,2)}ms Response time (furry.bot)"
    except Exception as e:
        furrybot = "Unable to get furry.bot response time."

    embed.set_field_at(index=0,name="Ping!",value = f"{pingtime}ms Latency\n{edittime}ms Edit Latency\n{nekoslife}\n{furrybot}")
    await msg.edit(content=None,embed=embed)





    



@commands.has_permissions(administrator = True)
@bot.command(brief="Changes nickname of everyone the bot can change",description="**WARNING: CAN BE HIGHLY DESTRUCTIVE!**")
async def massnick(ctx,*,nick : str = None):
    try:
     if len(nick) > 32:
        return await ctx.send(f"Nickname is too large. It must be under 32 letters (it is currently {len(nick)} letters long)")
    except TypeError: #Just in case it is None
        pass
    except Exception as e:
        raise e


    #Now time for the "destructive" part. Oh lord.
    msg = await ctx.send("Changing nicknames...")
    mlist = []
    count = 0
    for x in ctx.guild.members:
        try:
            await x.edit(nick=nick,reason=f"Massnick command ran by {ctx.author}")
            count = count + 1
            mlist.append(f"{count}. {x.name} {(f'({ctx.author.display_name})' if ctx.author.nick else '')} changed.")
        except discord.Forbidden:
            count = count + 1
            mlist.append(f"{count}. {x.name} {(f'({ctx.author.display_name})' if ctx.author.nick else '')} failed: Hoist role is lower than theirs.")
            pass
        except Exception as e:
            raise e
        await msg.edit(content=f"**{count}** nicknames changed (Last changed: ``{x.display_name}``)")

    #And then, beautiful, beautiful hastebin code
    st = "\n".join(mlist)
    x = await bot.session.post("https://hasteb.in/documents",data=f"List of nicknames changed in {ctx.guild.name}\n\n{st}")
    buff = await x.json()
    await msg.edit(content=f"All finished!\n**Results: https://hasteb.in/{buff['key']}*")    
        


@bot.command()
async def weather(ctx,*, cityname):
 async with ctx.message.channel.typing():
    try:
        res = await bot.session.get(f"https://api.openweathermap.org/data/2.5/weather?APPID={tokens['weathermap']}&q={cityname}")
        x = await res.json() 

        em = discord.Embed(title=f"Weather for {x['name']}, {x['sys']['country']}",description=f"ID: {x['id']}",color=discord.Color.dark_blue())
        em.add_field(name="🍃Wind Speed",value=f"{x['wind']['speed']}m/s")
        em.add_field(name="☁Cloud Percentage",value=f"{x['clouds']['all']}%")
        em.add_field(name="🌡Temp. Now",value=f"{round((x['main']['temp'] - 273.15),2)}**C**\n{round(((x['main']['temp'] - 273.15) * 9/5 + 32),2)}**F**")
        em.add_field(name="🌊Humidity",value=f"{x['main']['humidity']}%")
        time = datetime.datetime.utcfromtimestamp(x['sys']['sunrise']).strftime("%I:%M.%S%p %Z")
        em.add_field(name="🌄Sunrise Time",value=time)
        time = datetime.datetime.utcfromtimestamp(x['sys']['sunset']).strftime("%I:%M.%S%p %Z")
        em.add_field(name="🌇Sunset Time",value=time)
        em.set_footer(text="Data from openweathermap.org")
    except KeyError:
        await ctx.send("No city found. Did you make a typo?")
    except Exception as e:
        raise e


    await ctx.send(embed=em)
 
 

@bot.command(brief="Makes a fake Trump tweet.", description="Generates a Trump tweet from an API and sends it in chat.")
async def trump(ctx,*, text : str = "i wanna build a wall"):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}")
        x = await res.json()
        em = discord.Embed(title="Trump tweets something",color=discord.Color.dark_magenta())
        em.set_image(url=x["message"])
        em.set_footer(text="Powered by nekobot.xyz")
        await ctx.send(embed=em)



@bot.command(brief="Makes a 'change my mind' image")
async def changemind(ctx,*, text : str = "Youtube Rewind was bad"):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}")
        x = await res.json()
        url = x["message"]
        res = await bot.session.get(url)
        em = discord.Embed(title=f"{ctx.author.name} wants their mind changing",color=discord.Color.dark_magenta())
        em.set_image(url=url)
        em.set_footer(text="Powered by nekobot.xyz")
        await ctx.send(embed=em)
  

@bot.command(brief="Gets information on a Roblox user's profile (ID Only)",alises=['rbl'])
async def roblox(ctx,*,user : int):
    try:
        res = await bot.session.get(f"https://api.roblox.com/users/{user}")
        x = await res.json()
        groups = await bot.session.get(f"https://api.roblox.com/users/{user}/groups")
        groups = await groups.json()

        fmt = ""
        for group in groups:
            fmt = fmt + f"\n{group['Name']} ({group['Id']})"
    except:
        return await ctx.send("Player not found")

    em = discord.Embed(title=f"{discord.utils.get(bot.emojis,id=608793165885079571)}Information for {x['Username']}{discord.utils.get(bot.emojis,id=608793165885079571)}",color=discord.Color.red())
    em.add_field(name="ID",value=x['Id'])
    em.add_field(name="Groups",value=(fmt if not fmt == "" else "No Groups Found (Either the endpoint is down, or the user is in no groups)"))
    em.set_thumbnail(url=f"https://www.roblox.com/Thumbs/Avatar.ashx?x=500&y=500&userId={x['Id']}")

    await ctx.send(embed=em)


    
@bot.command(brief="Searches discordsbestbots.xyz for a bot",aliases=["dbb","dbbsearch","botsearch"])
async def discordbotsearch(ctx,*, botn: str = None):
    async with ctx.message.channel.typing():
        if botn == None:
            return await ctx.send("Bot name is required!")
        res = await bot.session.get(f"https://discordsbestbots.xyz/api/search?type=bot&search={botn}")
        searchjson = None
        try:
            searchjson = (await res.json())["bots"][0]
        except:
            return await ctx.send("No bots were found, or the site is down!")
        req = await bot.session.get(f"https://discordsbestbots.xyz/api/bots/{(searchjson['vanityUrl'] if searchjson['trusted'] else searchjson['_id'])}")
        botjson = ((await req.json())['bot'])
        em = discord.Embed(description=botjson["shortDesc"],color=discord.Color.teal())
        em.set_author(name=f"Info for {botjson['member']['user']['username']}#{botjson['member']['user']['discriminator']}",icon_url=botjson['member']['user']["displayAvatarURL"])
        em.add_field(name="Prefix",value=botjson["prefix"])
        em.add_field(name="Library",value=botjson["lang"])
        em.add_field(name="Github",value=(botjson["github"] if not botjson["github"] == "" else "No Github Linked"))
        em.add_field(name="Twitter",value=(botjson["twitter"] if not botjson["twitter"] == "" else "No Twitter Linked"))
        em.add_field(name="Website",value=(botjson["website"] if not botjson["website"] == "" else "No Website Linked"))
        #Do a little dance to append all owners into a format
        emojis = ""
        owners = []
        if botjson['owner']["trustedDev"] == True: emojis = emojis + str(discord.utils.get(bot.emojis,id=559115961421266965))
        if botjson['owner']["mod"] == True: emojis = emojis + str(discord.utils.get(bot.emojis,id=559115961475792898))
        if botjson['owner']["admin"] == True: emojis = emojis + str(discord.utils.get(bot.emojis,id=559115961408552962))
        owners.append(f"{botjson['owner']['user']['username']}#{botjson['owner']['user']['discriminator']} {(emojis if not emojis == '' else '')}")
        for x in botjson["owners"]:
            emojis = ""
            if x["trustedDev"] == True: emojis = emojis + str(discord.utils.get(bot.emojis,id=559115961421266965))
            if x["mod"] == True: emojis = emojis + str(discord.utils.get(bot.emojis,id=559115961475792898))
            if x["admin"] == True: emojis = emojis + str(discord.utils.get(bot.emojis,id=559115961408552962))
            owners.append(f"{x['user']['username']}#{x['user']['discriminator']} {(emojis if not emojis == '' else '')}")
        #Stop the dance since we formatted the owners
        em.add_field(name="Owners",value="\n".join(owners))
        em.add_field(name="Stats",value=(f"Guilds: {botjson['stats']['guilds']}\nShards: {botjson['stats']['shards']}"))
        em.add_field(name="Verified",value=f"{('Verified' if botjson['verified'] else 'Unverified')} ({('In Server' if botjson['inGuild'] else 'Not In Server')})")
        em.add_field(name="Trusted",value=("Yes" if botjson["trusted"] else "No"))
        em.add_field(name="Server",value=(botjson["server"] if botjson["server"] else "No Server Set"))
        em.add_field(name="Votes",value=f"Monthly Votes: {botjson['monthlyVotes']}\nTotal Votes: {botjson['totalVotes']}")
        
        try:
            em.add_field(name="NSFW",value=("Yes" if botjson["nsfw"] else "No"))
        except:
            em.add_field(name="NSFW",value="No")
        em.set_footer(text=f"Bot page: https://discordsbestbots.xyz/bots/{(botjson['vanityUrl'] if botjson['trusted'] else botjson['_id'])}")    
        em.set_image(url=(botjson["bg"] if not botjson["bg"] == "" else "https://pixelpikachu.tk/DXfAHOkI.png"))

        await ctx.send(embed=em)


@bot.command(brief="Modifies the modlog settings for the server ", description="Coded by: dat banana boi")
@commands.has_permissions(manage_guild=True)
async def modlog(ctx, channel): #i knew this was a bad idea
    if channel.lower() == "off" or channel.lower() == "disable":
        find = await bot.db.modlog.find_one({"id": ctx.guild.id})
        if not find: 
            return await ctx.send("Modlogs were never on.")
        else: 
            await bot.db.modlog.delete_one({"id": ctx.guild.id})
            await ctx.send("Modlogs have been turned OFF now.")
    else:
        chan = bot.get_channel(int(channel.strip("<#").strip(">"))) # revert to original
        await bot.db.modlog.update_one({"id": ctx.guild.id}, {"$set": {"channel": chan.id}}, upsert=True) #Chiki-chan~
        await ctx.send(f"Modlogs are now turned ON in {chan.mention}. Enjoy!") #Now events

@bot.command(brief="Gets someone's avatar",aliases=["av"])
async def avatar(ctx,user : discord.User = "plc"):
    if user == "plc":
        user = ctx.author
    em = discord.Embed(title=f"{user}'s Avatar",color=randomColor())
    em.set_image(url=user.avatar_url_as(size=1024))

    await ctx.send(embed=em)


@bot.command(brief="Posts some text to Hastebin",aliases=['hb'])
async def hastebin(ctx,*,text : str = "http://www.script-o-rama.com/movie_scripts/a1/bee-movie-script-transcript-seinfeld.html"):
    x = await bot.session.post("https://hasteb.in/documents",data=str(text))
    buff = await x.json()
    await ctx.send(f"Sent the text to Hastebin!\nhttps://hasteb.in/{buff['key']}")


@commands.is_nsfw() #DDB staff asked me to
@bot.command(brief="Googles a query for you",aliases=['g'])
async def google(ctx,*,text : str):
    async with ctx.message.channel.typing():
        re = search(query=text,tld='com',num=3,stop=3,safe=False,pause=2)
        st = []
        for s in re:
            st.append(f"<{s}>")
        fmt = '\n'.join(st)
        await ctx.send(f"Here are the top 3 results from a search:\n{fmt}")

@bot.command(brief="Gets a LMGTFY link for you",aliases=['letmegoogle','lmg'])
async def lmgtfy(ctx,*,text : str):
    text = text.split(' ')
    await ctx.send(f"http://lmgtfy.com/?q={'+'.join(text)}")

@bot.command(brief="Ships two users together")
async def ship(ctx, user : discord.Member, user2 : discord.Member):
    randomin = random.randint(0,100)
    fmt = ""
    if user == user2 or user2 == user:
        return await ctx.send("I cant ship the same person...")
    if (user.id == 478675118332051466 or user.id == 468785679036317699) and (user.id == 478675118332051466 or user.id == 468785679036317699):
        randomin = 100
    
    em = discord.Embed(title=f"{user.display_name} x {user2.display_name}",color=randomColor())
    
    if randomin >= 0:
        fmt = "Eeeeeeehhhhhhh..."
    if randomin >= 10:
        fmt = "Best as just friends.."
    if randomin >= 20:
        fmt = "Could be something.."
    if randomin >= 30:
        fmt = "Special... Possible crushes?"
    if randomin >= 40:
        fmt = "Should date..."
    if randomin >= 50:
        fmt = "Come on... I know one of you loves the other one"
    if randomin >= 60:
        fmt = "Needs some improvements..."
    if randomin == 69:
        if ctx.channel.nsfw:
            fmt = "*moans* your cock is so erect... >.<"
        else:
            fmt = "Hot and steamy..."
    if randomin >= 70:
        fmt = "A good couple"
    if randomin >= 80:
        fmt = "Just about perfect"
    if randomin >= 90:
        fmt = "Perfect couple!"
     
    em.add_field(name=f"{randomin}%",value=fmt)
    em.add_field(name="Ship Name",value=f"{(str(user.name))[:int(len((str(user.name))) / 2)] + (str(user2.name))[int(len((str(user2.name))) / 2):]}",inline=False)
    em.set_thumbnail(url=user.avatar_url_as(size=1024))
    em.set_footer(text="Will make the image better once the bot has access to image manipulation")
    await ctx.send(embed=em)


@bot.command(brief="Gets a random noun, adjective and verb from the English dictionary",aliases=['rg','ranwords'])
async def randomgrammar(ctx):
    async with ctx.message.channel.typing():
        await ctx.send(f"Noun: ``{random.choice(nouns)}``\nVerb: ``{random.choice(verbs)}``\nAdjective: ``{random.choice(adjectives)}``")


@bot.command(brief="Gets the top 15 servers the bot is in",aliases=["topservers","ts","tg"])
async def topguilds(ctx):
    sortlist = sorted(bot.guilds,key=lambda x: len(x.members),reverse=True)
    l = []
    for x in sortlist[0:14]:
        l.append(f"**{len(x.members)} members** - {x.name}")
    em = discord.Embed(title="Top 15 servers (Listed by member order)",description="\n".join(l),color=randomColor())
    await ctx.send(embed=em)


@bot.command(brief="Gives someone a lil' cuddle")
async def cuddle(ctx, user : discord.Member = "plc"):
    if user == "plc":
        user = ctx.author

    useAnime = not await bot.db.allowFurryList.find_one({"id": ctx.guild.id})
    buff = await bot.session.get(("https://nekos.life/api/v2/img/cuddle" if useAnime else "https://api.furry.bot/furry/sfw/cuddle"))
    json = await buff.json()
    em = discord.Embed(title=(f"{ctx.author.name} cuddled {user.name}! They're so cute!" if not ctx.author == user else f"Its okay {ctx.author.name}, I'll cuddle you"),color=discord.Color.dark_blue())
    em.set_image(url=(json['url'] if useAnime else json['response']['image']))
    em.set_footer(text=f"Powered by {('nekos.life' if useAnime else 'furry.bot')}")
    await ctx.send(embed=em)


@bot.command(brief="Gives someone a lil' hug")
async def hug(ctx, user : discord.Member = "plc"):
    if user == "plc":
        user = ctx.author

    useAnime = not await bot.db.allowFurryList.find_one({"id": ctx.guild.id})
    buff = await bot.session.get(("https://nekos.life/api/v2/img/hug" if useAnime else "https://api.furry.bot/furry/sfw/hug"))
    json = await buff.json()
    em = discord.Embed(title=(f"{ctx.author.name} just gave {user.name} a hug OwO" if not ctx.author == user else f"Its okay {ctx.author.name}, I'll hug you"),color=discord.Color.dark_blue())
    em.set_image(url=(json['url'] if useAnime else json['response']['image']))
    em.set_footer(text=f"Powered by {('nekos.life' if useAnime else 'furry.bot')}")
    await ctx.send(embed=em)


@bot.command(brief="Gives someone a kiss")
async def kiss(ctx, user : discord.Member = "plc"):
    if user == "plc":
        user = ctx.author

    useAnime = not await bot.db.allowFurryList.find_one({"id": ctx.guild.id})
    buff = await bot.session.get(("https://nekos.life/api/v2/img/kiss" if useAnime else "https://api.furry.bot/furry/sfw/kiss") )
    json = await buff.json()
    em = discord.Embed(title=(f"{ctx.author.name} just kissed {user.name}! Can I ship them?" if not ctx.author == user else f"Its ok... Have a kiss {ctx.author.name}"),color=discord.Color.dark_blue())
    em.set_image(url=(json['url'] if useAnime else json['response']['image']))
    em.set_footer(text=f"Powered by {('nekos.life' if useAnime else 'furry.bot')}")
    await ctx.send(embed=em)

@bot.command(brief="Grabs a random dog")
async def dog(ctx):
    buff = await bot.session.get("https://nekos.life/api/v2/img/woof")
    json = await buff.json()
    em = discord.Embed(title="Random Dog",color=discord.Color.purple())
    em.set_image(url=json['url'])
    em.set_footer(text="Powered by nekos.life")
    await ctx.send(embed=em)

@bot.command(brief="Grabs a random cat")
async def cat(ctx):
    buff = await bot.session.get("https://nekos.life/api/v2/img/meow")
    json = await buff.json()
    em = discord.Embed(title="Random Cat",color=discord.Color.purple())
    em.set_image(url=json['url'])
    em.set_footer(text="Powered by nekos.life")
    await ctx.send(embed=em)

@bot.command(brief="Grabs a fox girl picture")
async def foxgirl(ctx):
    buff = await bot.session.get("https://nekos.life/api/v2/img/fox_girl")
    json = await buff.json()
    em = discord.Embed(title="Random Fox Girl Picture",color=discord.Color.purple())
    em.set_image(url=json['url'])
    em.set_footer(text="Powered by nekos.life")
    await ctx.send(embed=em)


@commands.guild_only()
@bot.command(brief="Retrieves this server's information")
async def serverinfo(ctx,*,guild : int = "plc"):
    if guild == "plc" or not ctx.author.id in config["Admin"]:
        guild = ctx.guild
    elif not guild == "plc" and not ctx.author.id in config["Admin"]:
        guild = ctx.guild
    elif not guild == "plc" and ctx.author.id in config["Admin"]:
        guild = discord.utils.get(bot.guilds,id=guild)

    em = discord.Embed(title=f"Server information for {guild}",color=discord.Color.dark_purple())
    animated = 0
    normal = 0
    for emoji in guild.emojis:
        if emoji.animated:
            animated = animated + 1
        else:
            normal = normal + 1
    em.add_field(name="Emoji count",value=f"{animated} animated emojis\n{normal} non-animated emojis")
    bots = 0
    human = 0
    for mem in guild.members:
        if mem.bot:
            bots = bots + 1
        else:
            human = human + 1
    em.add_field(name="Member count",value=f"{human} humans\n{bots} bots")
    

    em.set_thumbnail(url=guild.icon_url)
    if guild.splash:
        em.set_image(url=guild.splash_url)
    if guild.banner:
        em.set_image(url=guild.banner_url)

    await ctx.send(embed=em)


@bot.command(brief="Makes a poll in the current channel",description="Seperate answers and the question by using \"|\"")
async def poll(ctx,*,text):
    text = text.split("|")
    try:
        text[1] = text[1]
    except:
        return await ctx.send("Please seperate the question and answer (e.g ``--poll Is this a cool command|Yes|No``)")
    
    try:
        if text[10]:
            return await ctx.send("Please supply less than 9 answers.")
    except:
        pass

    reactions = []
    fmt = ""
    count = 0
    for x in text[1:len(text)]:
        count = count + 1
        numstr = ""
        if count == 1:
            numstr = "one"
            reactions.append("1⃣")
        if count == 2:
            numstr = "two"
            reactions.append("2⃣")
        if count == 3:
            numstr = "three"
            reactions.append("3⃣")
        if count == 4:
            numstr = "four"
            reactions.append("4⃣")
        if count == 5:
            numstr = "five"
            reactions.append("5⃣")
        if count == 6:
            numstr = "six"
            reactions.append("6⃣")
        if count == 7:
            numstr = "seven"
            reactions.append("7⃣")
        if count == 8:
            numstr = "eight"
            reactions.append("8⃣")
        if count == 9:
            numstr = "nine"
            reactions.append("9⃣")
        fmt = fmt + f":{numstr}: - {text[count]}\n"
    
    em = discord.Embed(title=f"Poll - {text[0]}",description=f"{fmt}",color=discord.Color.dark_magenta())
    em.set_footer(text=f"Requested by: {ctx.author.display_name}",icon_url=ctx.author.avatar_url_as(size=1024))

    msg = await ctx.send(embed=em)
    for x in reactions:
        await msg.add_reaction(x)

    await ctx.message.delete()
    


@bot.command(brief="Sets your birthday for the bot (DD/MM)",description="PLEASE NOTE: WE WILL NOT SELL THIS DATA TO ANYONE ELSE!!")
async def setbirthday(ctx,day : int, month : int):
    if day > 31:
        return await ctx.send("Please enter a valid day")
    if month > 12:
        return await ctx.send("Please enter a valid month")

    await bot.db.birthdays.update_one({"id": str(ctx.author.id)}, {"$set": {"id": str(ctx.author.id), "month": month, "day": day}}, upsert=True)
    await ctx.send(f"Set your birthday to {day}/{month} (Please make sure the format is as DD/MM)")


#@commands.has_permissions(manage_server = True)
@commands.cooldown(1, 5, commands.BucketType.default)
@bot.command(brief="Sends all the users that have a birthday today in the server (Needs to be set with --setbirthday)")
async def birthdays(ctx):
    tmrn = time.gmtime(time.time())
    usrl = []
    for x in ctx.guild.members:
        dbu = await bot.db.birthdays.find_one({"id": str(x.id)})
        if dbu:
            if tmrn.tm_mon == dbu['month'] and tmrn.tm_mday == dbu['day']:
                usrl.append(f"{x.display_name}")

    em = discord.Embed(title=f"Birthdays for {tmrn.tm_mday}/{tmrn.tm_mon}",description="\n".join(usrl),color=discord.Color.green())
    em.set_footer(text=f"{len(usrl)} birthdays in total")

    await ctx.send(embed=em)

@bot.command(brief="Lets you view a lil' profile about yourself")
async def profile(ctx, user : discord.Member = "plc"):
    if user == "plc":
        user = ctx.author
    cmdr = await bot.db.commandsRan.find_one({"id": str(user.id)})
    em = discord.Embed(title=f"Profile for {user}",color=discord.Color.magenta())
    em.add_field(name="Commands Ran (in total)",value=(str(cmdr['count']) if cmdr is not None else "0"))
    em.add_field(name="Bot Role",value=("Developer" if user.id in config['Admin'] else ("Normal User" if not user.id in config["SpecialThanks"] else "Special Thank <3"))) #Purposely made this ugly, get fucked Banana.
    mguilds = 0
    for x in bot.guilds:
        if discord.utils.get(x.members,id=user.id):
            mguilds = mguilds + 1

    em.add_field(name="Mutual Server Count",value=f"{mguilds} servers")
    em.set_thumbnail(url=user.avatar_url_as(size=4096))
    await ctx.send(embed=em)


@bot.command(brief="Gets information about a pip package",aliases=['pip','pipsearch'])
async def pypi(ctx, package : str):
    #try:
    res = await bot.session.get(f"https://pypi.org/pypi/{package}/json")
    data = await res.json()
    info = data['info']
    releases = data['releases']
    urls = data['urls']
    #except:
    #    return await ctx.send("Package Not Found")
    em = discord.Embed(title=f"Result for {info['name']}",description=info['summary'],color=discord.Color.teal())
    if not info["author_email"] == "":
        aem = f"(Email: ``{info['author_email']})``"
    else:
        aem = ""
    em.add_field(name="Author",value=f'{info["author"]} {aem}')
    try:
        em.add_field(name="Requires",value="\n".join(info['requires_dist']))
    except:
        pass
    em.add_field(name="License",value=info['license'])
    #latestver = discord.utils.get(releases,info['version'])
    #em.add_field(name=f"Lastest Version ({info['version']})",value=f"Requires Python: ``{latestver['requires_python']}``\nPython Version: ``{latestver['python_version']}``\nPackage Type: ``{latestver['packagetype']}``\nMD5: ``{latestver['md5_digest']}``")
    em.add_field(name="Latest Version",value=str(info['version']))

    await ctx.send(embed=em)



# Furry Images Enabled Commands#

#@commands.has_permissions(manage_server = True, administrator=True)
@bot.command(brief="Enables/disables the use of furry images for this server. (needs manage server perms, but python decided to faint on me while making this)")
async def furryimages(ctx, set : str):
    if (not set == "enabled") and (not set == "disabled"):
        return await ctx.send("Please enter either enabled or disabled.")

    if not ctx.author.guild_permissions.manage_guild:
        return await ctx.send("You need Manage Server to run that")

    if set == "enabled":
        await bot.db.allowFurryList.update_one({"id": ctx.guild.id}, {"$set": {"id": ctx.guild.id}}, upsert=True) 
        await ctx.send("Enabled the use of furry images for this server")
    else:
        await bot.db.allowFurryList.delete_one({"id": ctx.guild.id})
        await ctx.send("Disabled the use of furry images for this server")
   
@bot.command(brief="Gives someone a lil' lick (REQUIRES FURRY IMAGES ENABLED)")
async def lick(ctx, user : discord.Member = "plc"):
    if not await bot.db.allowFurryList.find_one({"id": ctx.guild.id}):
        return await ctx.send("This server can not run that due to not allowing furry images. Please ask a server admin to run ``--furryimages enabled``")
    if user == "plc":
        user = ctx.author

    
    buff = await bot.session.get("https://api.furry.bot/furry/sfw/lick")
    json = await buff.json()
    em = discord.Embed(title=(f"{ctx.author.name} licked {user.name}!" if not ctx.author == user else f"Llllliiiiick!"),color=discord.Color.dark_blue())
    em.set_image(url=json['response']['image'])
    em.set_footer(text=f"Powered by furry.bot")
    await ctx.send(embed=em)

   
@bot.command(brief="Gives someone a lil' boop (REQUIRES FURRY IMAGES ENABLED)")
async def boop(ctx, user : discord.Member = "plc"):
    if not await bot.db.allowFurryList.find_one({"id": ctx.guild.id}):
        return await ctx.send("This server can not run that due to not allowing furry images. Please ask a server admin to run ``--furryimages enabled``")
    if user == "plc":
        user = ctx.author

    
    buff = await bot.session.get("https://api.furry.bot/furry/sfw/boop")
    json = await buff.json()
    em = discord.Embed(title=(f"{ctx.author.name} booped {user.name}!" if not ctx.author == user else f"Boop!"),color=discord.Color.dark_blue())
    em.set_image(url=json['response']['image'])
    em.set_footer(text=f"Powered by furry.bot")
    await ctx.send(embed=em)

   
@bot.command(brief="Holds someone's hand (REQUIRES FURRY IMAGES ENABLED)",aliases=['hh'])
async def holdhands(ctx, user : discord.Member = "plc"):
    if not await bot.db.allowFurryList.find_one({"id": ctx.guild.id}):
        return await ctx.send("This server can not run that due to not allowing furry images. Please ask a server admin to run ``--furryimages enabled``")
    if user == "plc":
        return await ctx.send("I can do everything, except hold your hand.")

    
    buff = await bot.session.get("https://api.furry.bot/furry/sfw/hold")
    json = await buff.json()
    em = discord.Embed(title=(f"{ctx.author.name} held {user.name}'s hand!"),color=discord.Color.dark_blue())
    em.set_image(url=json['response']['image'])
    em.set_footer(text=f"Powered by furry.bot")
    await ctx.send(embed=em)





#                   #
# NSFW INTERACTIONS #
#                   #

@commands.is_nsfw()
@bot.command(brief="Fucks another member, in bed.",aliases=["fuck"])
async def bang(ctx, user : discord.Member):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://api.furry.bot/furry/nsfw/bang")
        x = await res.json()
        url = x["response"]["image"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"{ctx.author.display_name} fucks {user.display_name}! Must be real tight!",color=randomColor())
        embed.set_footer(text="Powered by furry.bot")
        embed.set_image(url=url)
        await ctx.send(embed=embed)




#               #
# NSFW COMMANDS #
#               #

@commands.is_nsfw()
@bot.command(brief="Test Command",hidden=True)
async def nsfwtest(ctx):
    await ctx.send("Worked")


@commands.is_nsfw()
@bot.command(brief="Searches Urban Dictionary for a definition of a word")
async def urban(ctx,*,word : str):
    res = await bot.session.get(f"http://api.urbandictionary.com/v0/define?term={word}")
    data = await res.json()
    obj = data['list'][1]
    em = discord.Embed(title=f"Urban Dictionary: {word}",color=discord.Color.dark_magenta())
    em.add_field(name="Definition",value=(obj['definition'] if len(obj['definition']) >= 2000 else obj['definition'][1:2000]))
    em.add_field(name="Example",value=obj['example'],inline=False)
    em.set_footer(text=f"Written by: {obj['author']}")
    await ctx.send(embed=em)




@commands.is_nsfw()
@bot.command(brief="Grabs a random hentai gif")
async def hentaigif(ctx, mode : int = 0):
 async with ctx.message.channel.typing():
  if mode == 0:
   mode = random.randint(1,2)
  res = await bot.session.get(("https://nekos.life/api/v2/img/Random_hentai_gif" if mode == 1 else "https://nekobot.xyz/api/image?type=hentai"))
  x = await res.json()
  url = x[("url" if mode == 1 else "message")]
  res = await bot.session.get(url)
  bytes = await res.read()
  embed=discord.Embed(title=f"Hentai gif",color=randomColor())
  embed.set_footer(text=f"Powered by {('nekos.life' if mode == 1 else 'nekobot.xyz')}")
  embed.set_image(url=url)
  await ctx.send(embed=embed)
  


@commands.is_nsfw()
@bot.command(brief="Grabs a random hentai pic")
async def hentai(ctx):
 async with ctx.message.channel.typing():
  res = await bot.session.get(f"https://nekos.life/api/v2/img/hentai")
  x = await res.json()
  url = x["url"]
  res = await bot.session.get(url)
  bytes = await res.read()
  embed=discord.Embed(title=f"Hentai ",color=randomColor())
  embed.set_footer(text="Powered by nekos.life")
  embed.set_image(url=url)
  await ctx.send(embed=embed)
  
@commands.is_nsfw()
@bot.command(brief="Grabs a random futanari pic")
async def futanari(ctx):
 async with ctx.message.channel.typing():
  res = await bot.session.get(f"https://nekos.life/api/v2/img/futanari")
  x = await res.json()
  url = x["url"]
  res = await bot.session.get(url)
  bytes = await res.read()
  embed=discord.Embed(title=f"Futanari",color=randomColor())
  embed.set_footer(text="Powered by nekos.life")
  embed.set_image(url=url)
  await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a random anime pussy pic")
async def pussy(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/pussy")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Random pussy",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    



@commands.is_nsfw()
@bot.command(brief="Grabs a random nsfw neko gif")
async def nsfwneko(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/nsfw_neko_gif")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"NSFW Neko gif ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)
  


@commands.is_nsfw()
@bot.command(brief="Grabs a lewd-y anime picture")
async def lewd(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/lewd")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Lewd ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)


@commands.is_nsfw()
@bot.command(brief="Grabs a picture of an anime trap")
async def trap(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/trap")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"A trap ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)



@commands.is_nsfw()
@bot.command(brief="Grabs a pic of anime girls solo'ing")
async def solo(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/solo")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Solo pic ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)


@commands.is_nsfw()
@bot.command(aliases=["bj"],brief="Grabs a pic of anime boys getting blowjobbed")
async def blowjob(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/bj")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Blowjob ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)
 
@commands.is_nsfw()
@bot.command(brief="Grabs a pic of random hentai boobs")
async def boobs(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/boobs")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Boobs pic ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a pic of anime girls getting cummed on")
async def cum(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/cum")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Some cum ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a pic of anime girls getting anal'd")
async def anal(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/anal")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Anal pic ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)


@commands.is_nsfw()
@bot.command(brief="Grabs a picture of lewd nekos")
async def lewdneko(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekobot.xyz/api/image?type=lewdneko")
        x = await res.json()
        url = x["message"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Lewd neko ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)


@commands.is_nsfw()
@bot.command(brief="Grabs a picture of masturbating hentai girls",aliases=["pw","masturbate","mb"])
async def pwankg(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/pwankg")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Random pwankg gif",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a gif of anime girls solo'ing")
async def sologif(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/solog")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Solo pic ",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)


@commands.is_nsfw()
@bot.command(brief="Grabs a pic of holo lewd")
async def holo(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/hololewd")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Holo lewd",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a pic of a lewd kemo",aliases=["lk","lewdk"])
async def lewdkemo(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/lewdkemo")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Lewd kemo",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a gif of a neko",description="The only reason this is NSFW is due to the chance of lewd.",aliases=["nekog","ng"])
async def nekogif(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/ngif")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Neko gif",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a pic of a keta")
async def keta(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/keta")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Keta pic",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)


@commands.is_nsfw()
@bot.command(brief="Grabs a gif of anime girls getting sucked.",aliases=["pussysuck","ps"])
async def kuni(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/kuni")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Kuni pic",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a pic of an ero kemo")
async def erokemo(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/erokemo")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Ero kemo pic",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a pic of a holo ero")
async def holoero(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/holoero")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Holo ero",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a gif of lesbian anime girls",aliases=['les'])
async def lesbian(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/les")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Lesbian gif",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Grabs a gif of some classic hentai",aliases=['ch'])
async def classichentai(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://nekos.life/api/v2/img/classic")
        x = await res.json()
        url = x["url"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Classic Hentai",color=randomColor())
        embed.set_footer(text="Powered by nekos.life")
        embed.set_image(url=url)
        await ctx.send(embed=embed)


@commands.is_nsfw()
@bot.command(brief="Gets some furry porn from a random yiff subreddit (random from top 250 hot results)",aliases=["fh","yiff"])
async def furryhentai(ctx, *, sub : str = None):
    async with ctx.message.channel.typing():
        subreddits = ['yiff','gfur','yiffbulge','femyiff','FurryPornSubreddit']
        if sub is None or not sub in subreddits:
            choice = random.choice(subreddits)
        else:
            choice = sub
        hentai = reddit.subreddit(choice).hot(limit=250)
        submissions = [x for x in hentai]
        submission = random.choice(submissions)
        #submission = discord.utils.get(submissions,id = 'bolcze')
        #print(vars(submission))
        embed=discord.Embed(title=f"{submission.title}",color=discord.Color.dark_purple())
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"From r/{choice}")
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Gets some gay furry porn from r/gfur (random from top 250 hot results)",aliases=["gy"])
async def gyiff(ctx, *, srch : str = None):
    async with ctx.message.channel.typing():
        hentai = reddit.subreddit('gfur').hot(limit=250)
        submissions = [x for x in hentai]
        submission = random.choice(submissions)
        #submission = discord.utils.get(submissions,id = 'bolcze')
        #print(vars(submission))
        embed=discord.Embed(title=f"{submission.title}",color=discord.Color.dark_purple())
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"From r/gfur")
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Gets some Pokemon porn from r/PokePorn (random from top 250 hot results)",aliases=["pp","ph","pokemonhentai","phentai"])
async def pokeporn(ctx, *, srch : str = None):
    async with ctx.message.channel.typing():
        hentai = reddit.subreddit('PokePorn').hot(limit=250)
        submissions = [x for x in hentai]
        submission = random.choice(submissions)
        embed=discord.Embed(title=f"{submission.title}",color=discord.Color.dark_purple())
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"From r/PokePorn")
        await ctx.send(embed=embed)
    
@commands.is_nsfw()
@bot.command(brief="Gets some IRL porn from various subreddits",aliases=["porn"])
async def irl(ctx, *, sub : str = None):
    async with ctx.message.channel.typing():
        if sub is not None:
            if sub in config["Subreddits"]:
                sub = sub 
        else:
            sub = random.choice(config["Subreddits"])
        hentai = reddit.subreddit(sub).hot(limit=250)
        submissions = [x for x in hentai]
        submission = random.choice(submissions)
        embed=discord.Embed(title=f"{submission.title}",color=discord.Color.dark_purple())
        embed.set_image(url=submission.url)
        embed.set_footer(text=f"From r/{sub}")
        await ctx.send(embed=embed)

@commands.cooldown(2, 1, commands.BucketType.default)
@commands.is_nsfw()
@bot.command(brief="Gets a post from e621",aliases=['e6'])
async def e621(ctx,*,search : str):
    #https://e621.net/post/index.json?tags=fluffy+rating:s&limit=5
    #Example. No APIs work on PyPi so time to get hands down funky.
    async with ctx.message.channel.typing():  
     osearch = search
     search = search.split(' ')
     search = '+'.join(search)
     res = await bot.session.get(f"https://e621.net/post/index.json?tags={search}&limit=300&{e6login}",headers=uaheader)    
    
     x = await res.json()
     result = None
     try:
        result = random.choice(x)
     except:
         return await ctx.send("No posts found")
     em = discord.Embed(description=f"**Score {result['score']} **|** Rating: {result['rating']} **|** [Post]({result['sample_url']})**",color=randomColor())
     if not result['file_url'].endswith('.webm') and not result['file_url'].endswith('.swf'):
        em.set_image(url=result['file_url'])
     else:
        em.add_field(name="Unable to view file (webm/swf)",value="Discord's embed system doesn't work with webm/swf files. Please view on e621")
     em.set_footer(text=f"Post ID: {result['id']} | Author: {result['author']}")

     await ctx.send(embed=em)

@commands.is_nsfw()
@bot.command(brief="Gets an image of a bulge")
async def furbulge(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://api.furry.bot/furry/nsfw/bulge")
        x = await res.json()
        url = x["response"]["image"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Bulge image",color=randomColor())
        embed.set_footer(text="Powered by furry.bot")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Gets an image of furries NSFW cuddlin'")
async def nsfwcuddle(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://api.furry.bot/furry/nsfw/cuddle")
        x = await res.json()
        url = x["response"]["image"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Naked cuddles~",color=randomColor())
        embed.set_footer(text="Powered by furry.bot")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Gets an image of furries NSFW huggin'")
async def nsfwhug(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://api.furry.bot/furry/nsfw/hug")
        x = await res.json()
        url = x["response"]["image"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Naked hugs~",color=randomColor())
        embed.set_footer(text="Powered by furry.bot")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Gets an image of furries making out")
async def makeout(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://api.furry.bot/furry/nsfw/kiss")
        x = await res.json()
        url = x["response"]["image"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Make out session~",color=randomColor())
        embed.set_footer(text="Powered by furry.bot")
        embed.set_image(url=url)
        await ctx.send(embed=embed)

@commands.is_nsfw()
@bot.command(brief="Gets an image of furries NSFW licking")
async def nsfwlick(ctx):
    async with ctx.message.channel.typing():
        res = await bot.session.get(f"https://api.furry.bot/furry/nsfw/lick")
        x = await res.json()
        url = x["response"]["image"]
        res = await bot.session.get(url)
        bytes = await res.read()
        embed=discord.Embed(title=f"Naked licks~ OwO",color=randomColor())
        embed.set_footer(text="Powered by furry.bot")
        embed.set_image(url=url)
        await ctx.send(embed=embed)









#                   #
#    Help Command   #
#                   #

@bot.command(brief="Shows this message",description="Shows info about commands")
async def help(ctx,cmd : str = ""):
    # for command in bot.commands:
    command = bot.get_command(str(cmd))
    if bot.get_command(str(cmd)):
        return await ctx.send(f'```--Detailed Info for: {command.name} ({(", ".join(command.aliases) if not command.aliases == [] else "No Aliases For This Command") })--\n{command.signature}\n\n{(command.brief if not command.description else command.description)}```')
    elif command == None and cmd is not "":
        return await ctx.send("No command found")
    runcmds = []
    admincmds = []
    nruncmds = []
    nsfwcmds = []
    for command in bot.commands: 
            try:
             if await command.can_run(ctx) and not command.hidden:
                if ctx.channel.nsfw :
                  for x in command.checks:
                   if "is_nsfw" in str(x):
                     nsfwcmds.append(f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}')
                   else:
                     if not f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}' in runcmds:
                        runcmds.append(f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}')
                  else:
                      if not f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}' in nsfwcmds and not f'{command.name} - {(command.brief if command.brief else "No Brief Available")}' in runcmds:
                        runcmds.append(f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}')
                else:
                    runcmds.append(f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}')
             elif command.hidden:
                 admincmds.append(f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}')
            except discord.ext.commands.CommandError:
                for check in command.checks:
                 if "is_nsfw" in str(check):
                     nsfwcmds.append(f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}')
                for x in nsfwcmds:
                    if not f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}':
                     nruncmds.append(f'**{command.name}**\n{(command.brief if command.brief else "No Brief Available")}')
            except AttributeError as e:
                return await ctx.send("Awfully sorry, but since on how Python is structured, you have to run --help in a server")
                #Todo: fix this
            
            except Exception as e:
                raise e
    runcmds = sorted(runcmds)
    admincmds = sorted(admincmds)
    nruncmds = sorted(nruncmds)
    nsfwcmds = sorted(nsfwcmds)

    runcmdss = "\n".join(runcmds)
    #Aight, we have facts.txt for a reason. Time to use it.
    factlist = open("facts.txt","r")
    flist = factlist.readlines()
    try:
        embeds = [
            discord.Embed(title="Runnable Commands (pt 1)",description=runcmdss[0:1998],color=discord.Color.green(),footer=random.choice(flist)),
            discord.Embed(title="Runnable Commands (pt 2)",description=runcmdss[1999:len(runcmdss)],color=discord.Color.green()),
            discord.Embed(title="Not-Runnable Commands",description=("\n".join(nruncmds) if not nruncmds == [] else "N/A"),color=discord.Color.dark_red()),
            discord.Embed(title="NSFW Commands",description=("\n".join(nsfwcmds) if ctx.channel.nsfw or ctx.message.dm_channel else f"Hidden {len(nsfwcmds)} commands. For them to show, please run the command in a NSFW channel"),color=discord.Color.dark_teal()),
            discord.Embed(title="Admin Commands",description="\n".join(admincmds),color=discord.Color.purple())
        ]
    except AttributeError:
        embeds = [
            discord.Embed(title="Runnable Commands (pt 1)",description=runcmdss[0:1998],color=discord.Color.green()),
            discord.Embed(title="Runnable Commands (pt 2)",description=runcmdss[1999:len(runcmdss)],color=discord.Color.green()),
            discord.Embed(title="Not-Runnable Commands",description=("\n".join(nruncmds) if not nruncmds == [] else "N/A"),color=discord.Color.dark_red()),
            discord.Embed(title="NSFW Commands",description="\n".join(nsfwcmds),color=discord.Color.dark_teal()),
            discord.Embed(title="Admin Commands",description="\n".join(admincmds),color=discord.Color.purple())
        ]
    except Exception as e:
        raise e


    try:
        paginator = disputils.BotEmbedPaginator(ctx,embeds)
        await paginator.run()
    except:
        await ctx.send("The paginator has errored. Please make sure the bot has the Manage Messages permission.")




#                #
#                #
# Admin Commands #
#                #
#                #
#adm-cmd#

@bot.command(hidden=True)
async def error(ctx, *, error):
   if ctx.author.id in config['Admin']:
    bot.dispatch("command_error",ctx,error)

 
@bot.command(hidden=True)
async def dm(ctx,user : discord.User,*,msg : str):
    if ctx.author.id in config["Admin"]:
        await user.create_dm()
        embed=discord.Embed(title=f"Message from {ctx.author.name}", description=msg,color=0x7289da)
        await user.dm_channel.send(embed=embed)
        await ctx.send(f"**Successfuly sent a DM to {user.name}**")


@bot.command(hidden=True,brief="Broadcasts a message to all of bot's servers (not incluiding bot lists)")
async def broadcast(ctx,*, message : str):
    if ctx.author.id in config["Admin"]:
        for x in bot.guilds:
            if not "list" in x.name.lower() and not "plexi" in x.name.lower() and not "discord" in x.name.lower(): #good lord thats a lotta statements
                #for c in x.channels:
                 for c in ctx.guild.channels: #just for testing :P
                    try:
                        await c.send(f"__**PUBLIC BOT ANNOUNCEMENT**__\n\n{message}")
                        await ctx.send(f"Sent announcement to {c.name} ({c.id}) in {c.guild.name} ({c.guild.id})")
                        break
                    except discord.Forbidden:
                        pass
                    except AttributeError:
                        pass
                    except Exception as e:
                        raise e


@bot.command(brief="Restarts the bot",hidden=True)
async def restart(ctx):
    if ctx.message.author.id in config["Admin"]: 
        await ctx.send("Closing bot session...")
        await bot.session.close()
        await ctx.send("Saving file for restart...")
        file = open("restart.txt","w+")
        file.write(f"{ctx.channel.id}\n{ctx.message.id}")
        await ctx.send("Unloading cogs...")
        for cog in bot.cogs:
            bot.unload_extension(cog.name)
        await ctx.send("Closing file and logging out...")
        await bot.logout()


@bot.command(hidden=True)
async def mutuals(ctx,user : discord.User):
   if ctx.author.id in config["Admin"]:
    list = []
    em = discord.Embed(title=f"Mutual Servers with {user}",color=0x7289da)
    for x in bot.guilds:
        if discord.utils.get(x.members,id=user.id):
            list.append(x.name)
    em.add_field(name='Servers:',value=f"\n".join(list))
    await ctx.send(embed=em)


@bot.command(hidden=True)
async def presence(ctx, status = "plc",*, presence : str = "plc"):
#    if allowpresence == False and status == "plc":
#        allowpresence = True
#        return await ctx.send("Turned on the presence change")
#    allowpresence = False
#    await bot.change_presence(status=status,activity=discord.Game(name=presence))
#    await ctx.send(f"Changed the presence to: ``{presence}``\nand the status as: ``{status}``") 
    return await ctx.send("broken")

	  

@bot.command(hidden=True)
async def sudo(ctx, user : discord.Member,*, command : str):
   if ctx.message.author.id in config["Admin"]:
    p = await getprefix(bot,ctx.message)
    message = ctx.message
    message.author = user
    message.content = command
    await bot.process_commands(message)
    await ctx.message.add_reaction('\u2705')

	
	
@bot.command(name='eval', hidden=True)
async def _eval(ctx, *, body):
 if ctx.message.author.id in config["Admin"]:
    """Evaluates python code"""
 
    env = {
        'ctx': ctx,
        'bot': bot,
        'channel': ctx.message.channel,
        'author': ctx.message.author,
        'guild': ctx.message.guild,
        'message': ctx.message,
        'source': inspect.getsource
    }

    def cleanup_code(content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()
    err = out = None

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    def paginate(text: str):
        '''Simple generator that paginates text.'''
        last = 0
        pages = []
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text)-1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != '', pages))
    
    try:
        exec(to_compile, env)
    except Exception as e:
        err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        return await ctx.message.add_reaction('\u2049')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        if ret is None:
            if value:
                try:
                    
                    out = await ctx.send(f'```py\n{value}\n```')
                except:
                    paginated_text = paginate(value)
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')
        else:
            try:
                out = await ctx.send(f'```py\n{value}{ret}\n```')
            except:
                paginated_text = paginate(f"{value}{ret}")
                for page in paginated_text:
                    if page == paginated_text[-1]:
                        out = await ctx.send(f'```py\n{page}\n```')
                        break
                    await ctx.send(f'```py\n{page}\n```')

    if out:
        await ctx.message.add_reaction(bot.get_emoji(522530578860605442))  # tick
    elif err:
        await ctx.message.add_reaction(bot.get_emoji(522530579627900938))  # x
    else:
        await ctx.message.add_reaction(bot.get_emoji(522530578860605442)) #tick
    


#why did i add this?
@bot.command(hidden=True)
async def randomemoji(ctx):
    if ctx.author.id in config["Admin"]:
        selected = random.choice(bot.emojis)
        em = discord.Embed(color=randomColor())
        em.set_image(url=selected.url)
        em.set_footer(text=f"From: {selected.guild}",icon_url=selected.guild.icon_url)

        await ctx.send(embed=em)


		  

@bot.command(name="exec", hidden=True)
async def _exec(ctx, *, code):
  if ctx.author.id in config["Admin"]:
    async with ctx.message.channel.typing():    
        res = subprocess.run(f"{code}", cwd=os.getcwd(), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        err = res.stderr.decode("utf-8")
        opt = res.stdout.decode("utf-8")
        if len(opt or err) > 1973:
            x = await bot.session.post("https://hasteb.in/documents",data=str(err or opt))
            buff = await x.json()
            await ctx.send(f"The output is too large! Sent the results to hastebin\nhttps://hasteb.in/{buff['key']}")
        else:
            await ctx.send(f"Executed on commnand line!\n```{opt or err}```")
        

@bot.command(hidden=True)
async def blacklist(ctx,user : int,*, reason : str = "No Reason"):
    user = await bot.fetch_user(user)
    if ctx.author.id in config["Admin"]:
        if await bot.db.blacklist.find_one({"id": str(user.id) }):
            bot.db.blacklist.delete_one({"id": str(user.id)})
            await ctx.send(f"Unblacklisted ``{user}`` from the bot")
            em = discord.Embed(title="User Unlacklisted",description=f"``{user}`` unblacklisted",color=discord.Color.green())
            em.set_footer(text=f"Executed by {ctx.author}")
            await (bot.get_channel(637410687064342535)).send(embed=em)
        else:
            await bot.db.blacklist.update_one({"id": str(user.id)}, {"$set": {"reason": reason, "by": f"{ctx.author.name}#{ctx.author.discriminator}"}}, upsert=True)
            await ctx.send(f"Blacklisted ``{user}`` for ``{reason}``")
            em = discord.Embed(title="User Blacklisted",description=f"``{user}`` blacklisted for ``{reason}``",color=discord.Color.red())
            em.set_footer(text=f"Executed by {ctx.author}")
            await (bot.get_channel(637410687064342535)).send(embed=em)


@bot.command(hidden=True,aliases=['aui','adminui'])
async def advanceduserinfo(ctx, user : int):
    if ctx.author.id in config["Admin"]:
        user = await bot.fetch_user(user)
        if user == None: 
            return await ctx.send("Invalid user ID")
        
        em = discord.Embed(title=f"Advanced User Info for: {user.name}#{user.discriminator}",color=discord.Color.dark_purple())
        
        list = []
        for x in bot.guilds:
            if discord.utils.get(x.members,id=user.id):
                list.append(f"{x.name} ({x.id})")
        list = "\n".join(sorted(list))
        
        em.add_field(name="Mutual Guilds",value=(list if not list == "" else "No Mutual Guilds"))

        list = []
        if user.id in config['Admin']: list.append("Admin")
        if user.id in config['Mod'] or user.id in config['Admin']: list.append("Mod")
        if await bot.db.blacklist.find_one({"id": str(user.id) }): list.append("Blacklisted")
        list = ", ".join(list)

        em.add_field(name="Roles",value=(list if not list == "" else "No Roles"),inline=False)

        em.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=em)






#                    #
#                    #
#                    #
#     FUNCTIONS      #
#                    #
#                    #
#                    #
	

@bot.event
async def on_command_error(ctx, error): #Error handler     
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.DisabledCommand):
        return await ctx.send(f'{ctx.command} has been disabled.')
    if isinstance(error, commands.NoPrivateMessage):
        return await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
    if isinstance(error, commands.NotOwner):
        await ctx.message.add_reaction(':negative_squared_cross_mark:')
        return await ctx.send(f"{ctx.command} is for bot developers only you naughty person!")
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(error)
    if isinstance(error, commands.CheckFailure):
        return await ctx.send(error)
    if isinstance(error, commands.UserInputError):
        if not ctx.command.hidden or config["Admin"]:
            return await ctx.send(f"Usage: ``{(ctx.command.signature if ctx.command.signature else '')}``")
    if "Missing Permissions" in str(error):
        return await ctx.send("Failed to run due to I do not have high enough permissions.")
    
    code = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))

    #traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
    
    #Rewrote the embed because imo it was ugly
    try: #Put this in a try/except so it doesnt spew out a load of shit on shutdown
        em = discord.Embed(title=f"",color=discord.Color.dark_red())
        em.set_author(name=bot.user.name,url="https://thekirbybot.xyz",icon_url=bot.user.avatar_url)
        em.add_field(name="Error? Error? ERROR!",value=f"Hello {ctx.author.display_name},\nThe code in that command seems to be broken and the bot errored. Don't worry, you did not do anything wrong. The devs have been alerted and this hopefully gets fixed soon.\n\nEnjoy the rest of your day!",inline=False)
        em.add_field(name="Error (technical stuff)💻",value=f"```{error}```")
        em.set_footer(text=f"Error code: {code} | Please report this to #error-code-report in the support server")
        await ctx.send(embed=em)
    except:
        return


    #Rewrote Error Handler time :3


    em = discord.Embed(title="Error Receieved",color=discord.Color.red())
    em.set_author(name=bot.user.name,url="https://thekirbybot.xyz",icon_url=bot.user.avatar_url)
    em.add_field(name="Error",value=f"```{error}```",inline=False)
    if ctx.guild:
        em.add_field(name="Channel",value=f"Name: {ctx.message.channel.name}\nID: {ctx.message.channel.id}\nNSFW: {('Yes' if ctx.message.channel.nsfw else 'No')}")
        try:
            invite = discord.utils.get(await ctx.guild.invites(),max_age=0,max_uses=0).url
        except:
            invite = "No Permissions"
        em.add_field(name="Server",value=f"Name: {ctx.guild.name}\nInvite: {invite}")
    em.add_field(name="User",value=f"Tag: {ctx.author.name}#{ctx.author.discriminator}\nID: {ctx.author.id}")
    em.add_field(name="Message",value=f"Content: ``{ctx.message.content}``\nID: {ctx.message.id}")
    em.set_thumbnail(url=ctx.author.avatar_url)
    em.set_footer(text=f"Error Code: {code}")
    await bot.get_channel(632269115247296522).send(embed=em)

@bot.event
async def restartbot(ctx):
    await bot.logout()
    subprocess.call([sys.executable, "thekirbybot.py"])
	
@bot.event
async def nekobotfilter(ctx,type : str, param : str):
    res = await bot.session.get(f"https://nekobot.xyz/api/imagegen?type={type}&{param}")
    x = await res.json()
    url = x["message"]
    res = await bot.session.get(url)
    bytes = await res.read()
    await ctx.send(file=discord.File(bytes, f"{type}-{random.randint(0,999999999)}.png"))


@bot.event
async def on_message_edit(bctx,actx): #Bring it on Eric.
    p = await getprefix(bot,actx)
    if not bctx.content == actx.content:
        if actx.content.startswith(p):
            #Try to find the last message sent by the bot
            messagel = await (actx.channel.history(limit=10)).flatten() #Just to reduce ram usage
            last_msg = discord.utils.get(messagel,author=actx.guild.me)
            ctx = await bot.get_context(actx,cls=CustomContext)
            ctx.edit = True
            await bot.invoke(ctx)




@bot.event
async def on_command(ctx):
    bot.commands_run += 1
    dbentry = await bot.db.commandsRan.find_one({"id": str(ctx.author.id)})
    bot.db.commandsRan.update_one({"id": str(ctx.author.id)}, {"$set": {"count": (dbentry['count'] + 1 if dbentry else 1)}}, upsert=True)
    #print(f'{ctx.command.name} - {ctx.author}') #INCASE OF EMERGENCIES

@bot.event
async def on_message(ctx):
    p = await getprefix(bot,ctx)
    if f"<@{bot.user.id}>" == ctx.content or f"<@!{bot.user.id}>" == ctx.content:
        return await ctx.channel.send(f"Hi! I'm The Kirby Bot, a multipurpose bot for your needs. The server prefix here is ``{(f'{p[0]}`` or a mention' if isinstance(p,list) else f'{p}``')}.")    
    
    try: #just so if no pings are in a message it doesnt die
     if ctx.mentions[0]:
        mentiont = ctx.mentions[0]
        dbentry = await bot.db.afk.find_one({'id': mentiont.id})
        if dbentry:
            await ctx.channel.send(f"Hush, {mentiont} is AFK for ``{dbentry['status']}``")
    except IndexError:
     pass
    except Exception as e:
     raise e


    try: #Put this in a try/except statement to avoid spam in the terminal during start up
     if await bot.db.blacklist.find_one({"id": str(ctx.author.id)}):
        if ctx.content.startswith(p[0]) and ctx.content.replace(p[0], "").split(" ")[0] in [x.name for x in bot.commands]:
            d = await bot.db.blacklist.find_one({"id": str(ctx.author.id) })
            reason = d['reason']
            by = d['by']
            return await ctx.channel.send(f"Oh look at you. You are special. You have been banned from the bot by {usr}. Want to know why? Because {reason}. Now go away")
     if await bot.db.afk.find_one({"id": ctx.author.id}):
       await bot.db.afk.delete_one({"id": ctx.author.id})
       await ctx.channel.send(f"Welcome back {ctx.author.display_name}! I cleared your AFK status.")
       return
    except:
        pass
    
    await bot.process_commands(ctx)
	

@bot.event
async def on_member_join(member):
    if await bot.db.welc.find_one({ "id": str(member.guild.id) }):
        x = await bot.db.welc.find_one({ "id": str(member.guild.id) })
        msg = x['message']
        cid = x['channel']
        chnl = bot.get_channel(int(cid))
        #Now, jiggling the message to fix the format
        msg = msg.replace('{usr}',str(member))
        msg = msg.replace('{server}',str(member.guild))
        msg = msg.replace('{servercount}',str(len(member.guild.members)))
        await chnl.send(msg)
    
    if await bot.db.raidmode.find_one({ "id": str(member.guild.id) }):
        await member.send(f"Hey {member.name}, I am sorry but {member.guild.name} is in raidmode, so I had to kick you. Please try again later.")
        await member.kick(reason="[The Kirby Bot] Raidmode enabled.")


@bot.event
async def on_member_leave(member):
    if await bot.db.leave.find_one({ "id": str(member.guild.id) }):
        x = await bot.db.leave.find_one({ "id": str(member.guild.id) })
        msg = x['message']
        cid = x['channel']
        chnl = bot.get_channel(int(cid))
        #Now, jiggling the message to fix the format
        msg = msg.replace('{usr}',str(member))
        msg = msg.replace('{server}',str(member.guild))
        msg = msg.replace('{servercount}',str(len(member.guild.members)))
        await chnl.send(msg)

@bot.event
async def on_guild_join(guild):
    adminusr = []
    stusr = []
    bots = 0
    human = 0
    for x in guild.members:
        if x.id in config["Admin"]:
            adminusr.append(f"{discord.utils.get(bot.emojis,id=639224003223093266)} | {discord.utils.get(bot.users,id=x.id)}")
        if x.id in config["SpecialThanks"]:
            stusr.append(f"{discord.utils.get(bot.emojis,id=639224187889647626)} | {discord.utils.get(bot.users,id=x.id)}")
        if x.bot == True:
         bots += 1
        else:
         human += 1


    fmt = "\n".join(adminusr)
    fmt = fmt + "\n" + "\n".join(stusr)
    em = discord.Embed(title=f"{bot.user.name} has joined a guild!",color=discord.Colour.magenta())
    em.add_field(name="Name",value=guild.name)
    em.add_field(name="ID",value=guild.id)
    em.add_field(name="Member Count",value=f"{len(guild.members)} members ({human} humans, {bots} bots)")
    em.add_field(name="Bot Percentage",value=f"{round(len(guild.members)*bots/100)}%")
    em.add_field(name="Owner",value=f"{guild.owner.name}")
    if not fmt == "\n":
        em.add_field(name="Admins/Special in Guild",value=fmt,inline=False)
    em.set_footer(text=f"Guild Number: {len(bot.guilds)} | On Shard: {guild.shard_id}")
    em.set_thumbnail(url=guild.icon_url)
    await discord.utils.get(bot.get_guild(619924570110951435).channels,id=632269025463894026).send(embed=em)
    
    body = {"value1": str(guild.name), "value2": str(guild.icon_url)}
    await bot.session.post(url=tokens["ifttt"]["join"],data=body)


@bot.event
async def on_guild_unavailable(guild):
    em = discord.Embed(title=f"{(guild if guild.name else 'N/A')} unavailable",description="This guild has became unavailable. This might be due to Discord downtime.\n**Some attributes may not be able to be listed**",color=discord.Colour.orange())
    em.add_field(name="ID",value=(guild.id if guild.id else "Unavailable"))
    em.add_field(name="Owner",value=(guild.owner.name if guild.owner else "Unavailable"))
    em.add_field(name="Shard ID",value=(guild.shard_id if guild.shard_id else "Unavailable"))
    em.add_field(name="Member Count",value=(len(guild.members) if guild.members else "Unavailable"))
    em.set_thumbnail(url=(guild.icon_url if guild.icon_url else "https://baileymt.com/wp-content/uploads/2017/04/placeholder.jpg"))
    em.set_footer(text=f"Current Guild Count: {len(bot.guilds)}")

    await discord.utils.get(bot.get_guild(619924570110951435).channels,id=632269025463894026).send(embed=em)

@bot.event
async def on_guild_remove(guild):
    adminusr = []
    stusr = []
    bots = 0
    human = 0
    for x in guild.members:
        if x.id in config["Admin"]:
            adminusr.append(f"{discord.utils.get(bot.emojis,id=639224003223093266)} | {discord.utils.get(bot.users,id=x.id)}")
        if x.id in config["SpecialThanks"]:
            stusr.append(f"{discord.utils.get(bot.emojis,id=639224187889647626)} | {discord.utils.get(bot.users,id=x.id)}")
        if x.bot == True:
         bots += 1
        else:
         human += 1


    fmt = "\n".join(adminusr)
    fmt = fmt + "\n" + "\n".join(stusr)

    em = discord.Embed(title=f"{bot.user.name} has left a guild!",color=discord.Colour.purple())
    em.add_field(name="Name",value=guild.name)
    em.add_field(name="ID",value=guild.id)
    em.add_field(name="Member Count",value=f"{len(guild.members)} members ({human} humans, {bots} bots)")
    em.add_field(name="Bot Percentage",value=f"{round(len(guild.members)/100*bots)}%")
    em.add_field(name="Owner",value=f"{guild.owner.name}")
    em.set_footer(text=f"Guild Number: {len(bot.guilds)} | On Shard: {guild.shard_id}")
    if not fmt == "\n":
        em.add_field(name="Admins/Special in Guild",value=fmt,inline=False)
    em.set_thumbnail(url=guild.icon_url)
    await discord.utils.get(bot.get_guild(619924570110951435).channels,id=632269025463894026).send(embed=em)

    body = {"value1": str(guild.name), "value2": str(guild.icon_url)}
    await bot.session.post(url=tokens["ifttt"]["leave"],data=body)


@bot.event
async def process_commands(octx):
    ctx = await bot.get_context(octx,cls=CustomContext)

    await bot.invoke(ctx)







#MODLOG EVENTS#

@bot.event
async def on_message_delete(msg):
    if bot.db.modlog.find_one({"id": msg.guild.id}) and not msg.author.bot:
        em = discord.Embed(title="Deleted Message",description=msg.content,color=discord.Color.red(),timestamp=datetime.datetime.now())
        em.set_author(name=msg.author.display_name,icon_url=msg.author.avatar_url)

        chnl_id = await bot.db.modlog.find_one({"id": msg.guild.id})
        channel = bot.get_channel(chnl_id["channel"])
        await channel.send(embed=em)






try:
 if platform.platform() == 'Linux-4.15.0-66-generic-x86_64-with-Ubuntu-18.04-bionic' or 'Linux-4.19.57-v7+-armv7l-with-debian-10.0' or 'Linux-5.0.0-36-generic-x86_64-with-Ubuntu-19.04-disco':
    print("Starting Stable...")
    bot.run(tokens["bot"]["stable"])
 if platform.system() == 'Linux':
    print("Starting Beta...")
    bot.run(tokens["bot"]["beta"])
 else:
    print("Platform is not Linux. Aborting...")
except (KeyboardInterrupt, SystemExit):
    print("Closing Aiohttp session...")
    bot.session.close()
    print("Logging out of Discord...")
    bot.logout()
    print("Finished!")
