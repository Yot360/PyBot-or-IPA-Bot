from asyncio.tasks import sleep
from logging import error
import os
from os import listdir, path, write
import discord
from discord import message
from discord.ext import commands
from dotenv import load_dotenv
import json
import yaml

load_dotenv(dotenv_path="config")

bot = commands.Bot(command_prefix="*")
valid_user = ["yourUser#1234"]
text = discord.Embed()

def to_lower(argument):
    return argument.lower()

def to_capitalize(argument):
    return argument.capitalize()

@bot.event
async def on_ready():
    print("Bot ready.")

@bot.listen('on_message')
async def on_ping(message):
    if message.mention_everyone:
        return
    else:
        if bot.user.mentioned_in(message):
            await message.channel.send("My prefix is **_*_**")

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(bot.latency, 1)))

@bot.command(name='search')
async def search(ctx, file_name):
    search_result = '**Search Results:**'
    for file in listdir('/var/www/html/ipas'):
        if file_name in file.lower():
            search_result = search_result+'\n'+file
    if search_result == '**Search Results:**':
        await ctx.send('Error: No IPA similar to that name found.')
    else:
        await ctx.send(search_result)

@bot.command(name="list")
async def list(ctx):
    extension = '.ipa'
    search_result = '**Search Results:**'
    for file in listdir('/var/www/html/ipas'):
        if extension in file.lower():
            search_result = search_result+'\n'+file
    await ctx.send(search_result)


@bot.command(name='request')
async def request(ctx):
    dev = await bot.fetch_user(0000000000000000)
    author = ctx.message.author
    content = ctx.message.content
    with open('names.txt', 'r') as f:
        if str(author) in f.read():
            await ctx.send("Please wait another 2 hours before retrying")
            await sleep(7200)
            lines = f.readlines()
            with open('names.txt', 'w') as f:
                #if str(author) in f.read():
                for line in lines:
                    if line.strip("\n") != str(author):
                        f.write(line)
        else:
            await ctx.send("Link sent!")
            await dev.send(f"**{content}** sent from {author}")
            names = open("names.txt", "a")
            names.write(str(author)+"\n")
            names.close()


@bot.command(name='added')
async def added(ctx, arg, member: discord.Member = None):
    author = ctx.message.author
    if str(author) in valid_user: 
        if member is not None:
            await member.send(arg + " added!")
        else:
            await ctx.send("Please mention someone")

@bot.command(name='get')
async def get(ctx, ipa: to_lower):
    valid = False
    with open('ipa.json') as json_file:
        data = json.load(json_file)
        if ipa in data:
            for i in data[ipa]:
                valid = False
            for p in data["urls"]:
                ipa_url = (p[ipa])
                valid = True
        if ipa not in data:
            search_result = "**IPA not found, however similar ipa(s) may have been found**"
            await ctx.send(search_result)
            for file in listdir('/var/www/html/ipas'):
                if ipa in file.lower():
                    search_result ='\n'+file
            if search_result == '**IPA not found, however similar ipa(s) may have been found**':
                await ctx.send('No IPA found, use *search or *list to see if the ipa you want is listed, or request it with *request:')
            else:
                await ctx.send(search_result)
    text.colour = discord.Colour.blurple()
    text.set_thumbnail(url = "https://www.yot-dev.ml/ipas/logos/"+str(ipa)+".jpg")
    text.description = "**["+str.capitalize(ipa)+" IPA download link]("+ipa_url+")**\n"+yaml.safe_dump(i, allow_unicode=True, default_flow_style=False)
    await ctx.send(embed=text)

bot.remove_command("help")
@bot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(
        title = "Help",
        description = "Use `=help <command>` to know more about a command.", 
        colour = discord.Colour.red()
    )  
    em.add_field(name = "Getting IPA", value = "`get`")
    em.add_field(name = "Requests", value = "`request`")
    em.add_field(name = "IPA listing/searching", value = "`list, search`")
    em.set_thumbnail(url = "https://www.yot-dev.ml/pybot.png")
    em.set_author(name = "By: Yot#7962")
    await ctx.send(embed = em)


@help.command()
async def get(ctx):
    em = discord.Embed(title =  "Get", description = "Use this command to download an IPA.")
    em.add_field(name ="**Usage**", value = "`=get <IPA>`")
    await ctx.send(embed = em)

@help.command()
async def request(ctx):
    em = discord.Embed(title =  "Requests", description = "Use this command to request an IPA that is not in the library or a feature.")
    em.add_field(name ="**Usage**", value = "`=request <IPA to request, link if possible>`")
    await ctx.send(embed = em)

@help.command()
async def list(ctx):
    em = discord.Embed(title =  "List", description = "Use this command to list all IPAs.")
    em.add_field(name ="**Usage**", value = "`=list`")
    await ctx.send(embed = em)

@help.command()
async def search(ctx):
    em = discord.Embed(title =  "Search", description = "Use this command to search an IPA (the bot might give similar names if the IPA isn't found).")
    em.add_field(name ="**Usage**", value = "`=search <IPA>`")
    await ctx.send(embed = em)

bot.run(os.getenv("TOKEN"))