import sys, os, discord, shutil, psutil
from colorama import Fore, Back, Style
from datetime import datetime
from copy import copy
if not os.path.isdir("logs"): os.mkdir("logs")

def backup():
    backup = os.path.join("backup", datetime.now().isoformat().replace(":", "."))
    os.mkdir(backup)
    shutil.copyfile("credit.json", os.path.join(backup, "credit.json"))
    print(f'{Fore.LIGHTGREEN_EX}[{datetime.now()}] [I] [BACKUP] - Backed up database to "{backup}"!{Style.RESET_ALL}')
    del backup

class STD:
    def __init__(self, date):
        self.basesys = sys.stdout
        self.stdout = []
        self.log = os.path.join("logs", f"log-stdout-{date}.log")

    def flush(self, *args):
        self.basesys.flush()
    
    def write(self, *args):
        self.stdout.append(*args)
        self.basesys.write(*args)
        with open(self.log, "w") as f:
            f.write("".join(self.stdout)) # Метод офкорс я из пита скопироваль)

class STDerr:
    def __init__(self, date):
        self.basesys = sys.stderr
        self.stderr = []
        self.log = os.path.join("logs", f"log-stderr-{date}.log")

    def flush(self, *args):
        self.basesys.flush()
    
    def write(self, *args):
        self.stderr.append(*args)
        self.basesys.write(*args)
        with open(self.log, "w") as f:
            f.write("".join(self.stderr)) # Метод офкорс я из пита скопироваль) x2

def redefine_std():
    date = datetime.now().isoformat().replace(":", ".")
    sys.stdout = STD(date)
    sys.stderr = STDerr(date)

    

def debug_info():
    def count_percent(percent, all):
        return round(100/(all/percent)) 
    def get_progress(percent):
        blocks = round(percent / 10)
        not_busy_blocks = 10-blocks
        progress = (blocks * "█" * 2) + (not_busy_blocks * "░" *2)
        return progress, str(percent) + "%"

    string= "\n -> Python Core " + sys.version + "\n"
    if sys.platform in ["win32", "cygwin"]:
        platform = "Windows "
        ver = sys.getwindowsversion()
        platform += f"{ver.major}(.{ver.minor}) build {ver.build}"
        string+= f" -> Platform: {platform} \n"
        del platform
    impl = sys.implementation
    impl = f"{impl.name}/Tag: {impl.cache_tag}"
    string += f" -> Implementation: {impl} \n"
    string += f" -> Core C API Version: {sys.api_version} \n"

    mem = psutil.virtual_memory()
    percent = count_percent(mem.used, mem.total)
    string += f' -> VRam: {" ".join(get_progress(percent))}'

    print(f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[{datetime.now()}] [D] [DEBINF] - Debug info: {string}{Style.RESET_ALL}')
    del string, impl, ver

# ==========
# = ОШИБКИ =
# ==========

async def perms_error(ctx):
    emb = discord.Embed(
                title='Ошибка прав!',
                description='Ну и ну! Китай Правительство вам не выдать разрешение **Управление Ролями**, поэтому вы не мочь изменять социальный кредит! Много смех!',
                color=0xff0000
    )
    emb.set_image(url='https://media.discordapp.net/attachments/883778578783821865/896453128185081896/unknown.png')
    emb.set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

async def member_not_found(ctx, type):
    emb = discord.Embed(
        title='Гражданин не обнаружен!',
        description=f'Ну и ну! Бот не смочь найти гражданин для {type} социальный кредит!',
        color=0xff0000
    )
    emb.set_image(url='https://media.discordapp.net/attachments/883779765415337995/896458794886918225/unknown.png')
    emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb)