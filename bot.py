import discord, json, os, random,shutil, sys
from discord import colour
from discord.ext import commands
from datetime import datetime
from colorama import init, Style, Back, Fore
from discord.ext.commands.core import check
from functions import debug_info, redefine_std, backup, version_check, release_info
from copy import copy
with open("env.json", encoding="utf-8") as file: conf = json.load(file)
init()
version_check(conf["ro.python.minimal"][0], conf["ro.python.minimal"][1])
with open("token.json", encoding="utf-8") as file: token = json.load(file); TOKEN = token["vendor.token"]; del token

if conf["ro.bot.logd"]:
    redefine_std()
    print(f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[{datetime.now()}] [D] [LOGDMN] - LogD started.{Style.RESET_ALL}')

if conf["ro.build.type"][0] == "debug": debug_info(conf)
elif conf["ro.build.type"][0] == "release": release_info(conf)

if not os.path.isdir("backup"): os.mkdir("backup")
if not os.path.isfile("credit.json"): 
    with open("credit.json", "w") as file: file.write("{}") 

backup()

# async with ctx.channel.typing():

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='scd.',owner_ids=[528606316432719908,453167201780760577],intents=intents)
bot.conf = copy(conf)

# ======
# ЗАПУСК
# ======

bot.remove_command("help")

with open("credit.json", "r", encoding="utf-8") as file:
    db = json.load(file)
    bot.db = db

def save():
    with open("credit.json", "w", encoding="utf-8") as file:
        json.dump(bot.db, file, indent=4)

def load():
    with open("credit.json", "r", encoding="utf-8") as file:
        bot.db = json.load(file)

def check_lang(guild):
    load()
    gid = str(guild.id)
    return bot.db[gid]["lang"]

@bot.event
async def on_command_error(ctx, error):
    blacklist = ["MissingPermissions", "MemberNotFound", "CommandNotFound", "CommandOnCooldown"] # Расизм, расия)
    if isinstance(error, discord.ext.commands.CommandNotFound):
        err = str(error).replace("Command \"", "").replace("\" is not found", "")
        lang = check_lang(ctx.guild)
        if lang == "RU":
            emb = discord.Embed(
                title='Команда не найдена!',
                description=f'Ну и ну! Бот не смочь найти команда "{err}"!',
                color=0xff0000
            )
        elif lang == "EN":
            emb = discord.Embed(
                title='Command not found!',
                description=f'Well, the Bot couldn\'t find the "{err}" command!',
                color=0xff0000
            )
        emb.set_image(url='https://media.discordapp.net/attachments/883779765415337995/896458794886918225/unknown.png')
        emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.reply(embed=emb)
    if type(error).__name__ in blacklist: return
    print(f'{Fore.RED}[{datetime.now()}] [C] [ERRMSG] - Error Raised! More info below:{Style.RESET_ALL}')
    print(f"{Fore.LIGHTRED_EX}-> {error}{Style.RESET_ALL}")

@bot.event
async def on_ready():
    stream = discord.Streaming(platform='China',name='sc.',game='Social Credit',url='https://clmty.xyz/')
    await bot.change_presence(status=discord.Status.idle, activity=stream)
    print(f'{Fore.GREEN}[{datetime.now()}] [I] [CLIENT] - Launched.{Style.RESET_ALL}')
    for i in os.listdir("cogs"):
        if os.path.isfile(os.path.join("cogs", i)):
            if not f'cogs.{i[:-3]}' in bot.extensions:
                bot.load_extension(f'cogs.{i[:-3]}')
    

# =======
# КОМАНДЫ
# =======

def ownercheck(id):
    if id in [528606316432719908,453167201780760577]:
        return True
    else:
        return False

bot.ownercheck = ownercheck

# ТОКЕН
bot.run(TOKEN)