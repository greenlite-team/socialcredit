import sys, os, disnake, shutil, psutil, json
from colorama import Fore, Back, Style
from datetime import datetime
from copy import copy
if not os.path.isdir("logs"): os.mkdir("logs")

def version_check(major, minor):
    if sys.version_info.major != major:
        print(f'{Fore.RED}[{datetime.now()}] [C] [VCHECK] - Minimal version to boot is {major}.{minor}, but your is {sys.version_info.major}.{sys.version_info.minor}!{Style.RESET_ALL}')
        sys.exit()
    elif sys.version_info.minor < minor:
            print(f'{Fore.RED}[{datetime.now()}] [C] [VCHECK] - Minimal version to boot is {major}.{minor}, but your is {sys.version_info.major}.{sys.version_info.minor}!{Style.RESET_ALL}')
            sys.exit()

    print(f'{Fore.LIGHTCYAN_EX}[{datetime.now()}] [C] [VCHECK] - Version Check passed - {major}.{minor} >= {sys.version_info.major}.{sys.version_info.minor}{Style.RESET_ALL}')


def backup():
    backup = os.path.join("backup", datetime.now().isoformat().replace(":", "."))
    os.mkdir(backup)
    shutil.copyfile("credit.json", os.path.join(backup, "credit.json"))
    print(f'{Fore.LIGHTGREEN_EX}[{datetime.now()}] [I] [BACKUP] - Backed up database to "{backup}"!{Style.RESET_ALL}')
    del backup

class STD: # sexually transmitted disease
    def __init__(self, date):
        self.basesys = sys.stdout
        self.stdout = []
        self.log = os.path.join("logs", f"log-stdout-{date}.log")

    def flush(self, *args):
        self.basesys.flush()
    
    def write(self, *args):
        self.stdout.append(*args)
        self.basesys.write(*args)
        with open(self.log, "w", encoding="utf-8") as f:
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
        with open(self.log, "w", encoding="utf-8") as f:
            f.write("".join(self.stderr)) # Метод офкорс я из пита скопироваль) x2

def redefine_std():
    date = datetime.now().isoformat().replace(":", ".")
    sys.stdout = STD(date)
    sys.stderr = STDerr(date)

def release_info(conf):
    string= "\n -> Bot in Release mode. Version: "+ conf["ro.bot.version"] +"\n -> Python Core " + sys.version + "\n"
    impl = sys.implementation
    impl = f"{impl.name}/Tag: {impl.cache_tag}"
    string += f" -> Implementation: {impl}"

    print(f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[{datetime.now()}] [D] [RELINF] - Release info: {string}{Style.RESET_ALL}')
    del string, impl

def debug_info(conf):
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
        del platform, ver
    impl = sys.implementation
    impl = f"{impl.name}/Tag: {impl.cache_tag}"
    string += f" -> Implementation: {impl} \n"
    string += f" -> Core C API Version: {sys.api_version} \n"

    mem = psutil.virtual_memory()
    percent = count_percent(mem.used, mem.total)
    string += f' -> VRam: {" ".join(get_progress(percent))} \n'
    string += f" -> env.json Info: \n"
    string += f" --> Bot Version (ro.bot.version): {conf['ro.bot.version']} \n" 
    string += f" --> LogD (ro.bot.logd): {conf['ro.bot.logd']} \n" 
    string += f" --> Build Type (ro.build.type): {conf['ro.build.type']} \n" 
    string += f" --> Python Mininal Version (ro.python.minimal): {conf['ro.python.minimal']}" 

    print(f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[{datetime.now()}] [D] [DEBINF] - Debug info: {string}{Style.RESET_ALL}')
    del string, impl

# ==========
# = ОШИБКИ =
# ==========

async def perms_error(ctx):
    emb = disnake.Embed(
        title='Permissions Error!',
        description='The CCP didn\'t gave you the **Manage Roles** permission, so you cannot edit the Social Credit Scores! Lots Of Laughs! `(англ. язык временно, потом фикс)`',
        color=0xff0000
    )
    emb.set_image(url='https://media.discordapp.net/attachments/883778578783821865/896453128185081896/unknown.png')
    emb.set_footer(text=ctx.author,icon_url=ctx.author.avatar.url)
    await ctx.send(embed=emb)

async def member_not_found(ctx, type):
    emb = disnake.Embed(
        title='Citizen not found!',
        description=f'The Bot couldn\'t find the citizen for editing their Social Credit Score! `(англ. язык временно, потом фикс)`',
        color=0xff0000
    )
    emb.set_image(url='https://media.discordapp.net/attachments/883779765415337995/896458794886918225/unknown.png')
    emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
    await ctx.send(embed=emb)