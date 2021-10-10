import discord, json, os, random,shutil, sys
from discord import colour
from discord.ext import commands
from datetime import datetime
from colorama import init, Style, Back, Fore
from cogs.credit import credit

save = credit.save
init()

from functions import debug_info, redefine_std, backup
# redefine_std()
debug_info()

if not os.path.isdir("backup"): os.mkdir("backup")
if not os.path.isfile("credit.json"): 
    with open("credit.json", "w") as file: file.write("{}") 
with open("env.json", encoding="utf-8") as file: conf = json.load(file)
backup()



# async with ctx.channel.typing():

bot = commands.Bot(command_prefix='sc.', owner_ids=[528606316432719908,453167201780760577])
TOKEN = conf["token"]

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

@bot.event
async def on_command_error(ctx, error):
    blacklist = ["MissingPermissions", "MemberNotFound"] # Расизм, расия)
    if type(error).__name__ in blacklist: return
    print(f'{Fore.RED}[{datetime.now()}] [C] [ERRMSG] - Error Raised! More info below:{Style.RESET_ALL}')
    print(f"{Fore.LIGHTRED_EX}-> {error}{Style.RESET_ALL}")

@bot.event
async def on_ready():
    stream = discord.Streaming(platform='Sex',name='sc.',game='Social Credit',url='https://clmty.xyz/')
    await bot.change_presence(status=discord.Status.idle, activity=stream)
    print(f'{Fore.GREEN}[{datetime.now()}] [I] [CLIENT] - Launched.{Style.RESET_ALL}')
    bot.load_extension("cogs.credit")
    

# =======
# КОМАНДЫ
# =======

def ownercheck(id):
    if id in [528606316432719908,453167201780760577]:
        return True
    else:
        return False

@bot.command()
async def ping(ctx):
    emb = discord.Embed(
        title='Понг!',
        description=f'Пинг: {int(round(bot.latency, 4) * 1000)}',
        color=0xff0000
    )
    await ctx.send(embed=emb)

@bot.command(aliases=["quit", 'logout', 'выйти', 'выключить', 'вырубить', 'poweroff'])
async def logoff(ctx):
    if ownercheck(ctx.author.id):
        await ctx.reply("Выключаюсь...")

        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - 'logoff' command executed by {ctx.author}.{Style.RESET_ALL}")
        backup()
        if 'credit' in bot.cogs: 
            bot.cogs['credit'].save()
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - Saved and backed up database to do safe logout.{Style.RESET_ALL}")
        await bot.close()

        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [CLIENT] - Logged out.{Style.RESET_ALL}")
        sys.exit()



@bot.command()
async def reload(ctx):
    if ownercheck(ctx.author.id):
        if 'cogs.credit' in bot.extensions:
            bot.unload_extension('cogs.credit')
        else:
            print(f'{Fore.YELLOW}[{datetime.now()}] [W] [RELOAD] - Is cogs.credit loaded?!{Style.RESET_ALL}')
        bot.load_extension('cogs.credit')
        await ctx.send('Бот перезагружен!')
        print(f'{Fore.LIGHTYELLOW_EX}[{datetime.now()}] [I] [RELOAD] - Reloaded by {ctx.author}.{Style.RESET_ALL}')

# ТОКЕН

bot.run(TOKEN)