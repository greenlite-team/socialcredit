import discord, json, os, random,shutil
from discord import colour
from discord.ext import commands
from datetime import datetime
from colorama import init, Style, Back, Fore
init()

if not os.path.isdir("backup"): os.mkdir("backup")
if not os.path.isfile("credit.json"): 
    with open("credit.json", "w") as file: file.write("{}") 

# async with ctx.channel.typing():

bot = commands.Bot(command_prefix='sc.', owner_ids=[528606316432719908,453167201780760577])
TOKEN = 'ODk1Njg4MTIxMjg1NTA5MTUx.YV8MkQ.RgbU4oGvZHmVv1onv15DS61SDfM'

# ======
# ЗАПУСК
# ======
bot.remove_command("help")

backup = os.path.join("backup", datetime.now().isoformat().replace(":", "."))
os.mkdir(backup)
shutil.copyfile("credit.json", os.path.join(backup, "credit.json"))
print(f'{Fore.LIGHTGREEN_EX}[{datetime.now()}] [BACKUP] - Backed up database to "{backup}"!{Style.RESET_ALL}')
del backup

with open("credit.json", "r", encoding="utf-8") as file:
    db = json.load(file)
    bot.db = db

def save():
    with open("credit.json", "w", encoding="utf-8") as file:
        json.dump(bot.db, file, indent=4)

@bot.event
async def on_ready():
    stream = discord.Streaming(platform='Sex',name='sc.',game='Social Credit',url='https://clmty.xyz/')
    await bot.change_presence(status=discord.Status.idle, activity=stream)
    print(f'{Fore.GREEN}[{datetime.now()}] [CLIENT] - Launched.{Style.RESET_ALL}')
    bot.load_extension('cogs.credit')

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

@bot.command()
async def reload(ctx):
    if ownercheck(ctx.author.id):
        bot.unload_extension('cogs.credit')
        bot.load_extension('cogs.credit')
        await ctx.send('Бот перезагружен!')
        print(f'{Fore.LIGHTYELLOW_EX}[{datetime.now()}] [RELOAD] - Reloaded.{Style.RESET_ALL}')

# ТОКЕН
bot.run(TOKEN)