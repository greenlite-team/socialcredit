import disnake, colorama, sys, os, json
from datetime import datetime
from colorama import Back, Fore, Style
from disnake.ext import commands, tasks
from functions import backup
from time import sleep

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load(self):
        with open("credit.json", "r", encoding="utf-8") as file:
            self.bot.db = json.load(file)

    def check_lang(self, guild):
        self.load()
        gid = str(guild.id)
        return self.bot.db[gid]["lang"]

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"{Fore.LIGHTGREEN_EX}[{datetime.now()}] [I] [+GUILD] - Bot joined a new guild: '{guild.name}'. Member count: '{guild.member_count}'.{Style.RESET_ALL}")
        emb = disnake.Embed(
            title=':wave: Здравствуйте!',
            description="Я есть Социальный Кредит бот разработанный `Calamity#3483` и `KrutosX#3599` совместно с Коммунистическая Партия Китай.",
            color=0xb8493c
        )
        emb.add_field(
            name=":key: Что я уметь?",
            value="Данный бот уметь добавление/отнимание/установка Социальный Кредит, и Китай Пропаганда (молчание!).\nУзнать больше: `sc.help`",
            inline=False
        )
        emb.add_field(
            name=":flag_gb: English?",
            value="Switch to the English language using `sc.lang EN`. (only availible for admins)"
        )
        for i in guild.text_channels:
            perm = i.permissions_for(guild.me)
            if perm.send_messages:
                await i.send(embed=emb)
                break

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [I] [-GUILD] - Bot left guild: '{guild.name}'. Member count: '{guild.member_count}'.{Style.RESET_ALL}")
    
    @commands.cooldown(rate=1, per=10)
    @commands.command(description="пингануть")
    async def ping(self, ctx):
        lang = self.check_lang(ctx.guild)
        if lang == "RU":
            emb = disnake.Embed(
                title='Понг!',
                description=f'Пинг: {int(round(self.bot.latency, 4) * 1000)}',
                color=ctx.guild.me.color
            )
        elif lang == "EN":
            emb = disnake.Embed(
                title='Pong!',
                description=f'Latency: {int(round(self.bot.latency, 4) * 1000)}',
                color=ctx.guild.me.color
            )
        await ctx.send(embed=emb,ephemeral=True)
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - 'ping' command executed by {ctx.author}.{Style.RESET_ALL}")

    @commands.command(description="информация о боте")
    async def version(self, ctx):
        lang = self.check_lang(ctx.guild)
        if lang == "RU":
            emb = disnake.Embed(
                title='Версии',
                description=f'Версия: `{self.bot.conf["ro.bot.version"]}`\nВерсия Python: `{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}`\nВерсия disnake: `{disnake.__version__}`',
                color=0xff0000
            )
        elif lang == "EN":
            emb = disnake.Embed(
                title='Versions',
                description=f'Bot Version: `{self.bot.conf["ro.bot.version"]}`\nPython Version: `{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}`\ndisnake Version: `{disnake.__version__}`',
                color=0xff0000
            )
        await ctx.send(embed=emb)
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - 'version' command executed by {ctx.author}.{Style.RESET_ALL}")

    @commands.command(aliases=["quit", 'logout', 'выйти', 'выключить', 'вырубить', 'poweroff'])
    async def logoff(self, ctx):
        if self.bot.ownercheck(ctx.author.id):
            await ctx.reply("Logging off...")
            # 4(x^2) - 3x + 1 = 0
            # a = 4, b = -3, c = +3
            # D = b^2 - 4ac = -3^2 - 4 * 4 * 3 = 9 - 48 = -39
            # 3(x^2) + 7x − 6 = 0
            # D = b^2 - 4ac = 7^2 - 4 * 3 * (-6) = 49 - 12*(-6) = 49 + 72 = 121
            # D>0; 2k.
            # x1 = (-b + sqrt(D))/2a
            # x2 =  
            # 🂠 back
            # 🂱🂲🂳🂴🂵🂶🂷🂸🂹🂺🂻🂽🂾 hearts
            # 🃁🃂🃃🃄🃅🃆🃇🃈🃉🃊🃋🃍🃎 diamonds
            # 🃑🃒🃓🃔🃕🃖🃗🃘🃙🃚🃛🃝🃞 spades
            # 🂡🂢🂣🂤🂥🂦🂧🂨🂩🂪🂫🂭🂮 clubs
            # 25x - 17 = 4x - 5 - 13x + 14 + 34x
            # 25x - 17 = 38x - 13x + 9
            # 38x - 17 != 38x + 9
            # Корней нет, иди нахуй. - Каламя
            # Я хоть и знаю, что это не мне, но я не против! - Крутос
            # Делаем дз с Крутосом епта - 11.10.2021, 22:15
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - 'logoff' command executed by {ctx.author}.{Style.RESET_ALL}")
            backup()
            if 'credit' in self.bot.cogs: 
                self.bot.cogs['credit'].save()
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - Saved and backed up database to do safe logout.{Style.RESET_ALL}")
            await self.bot.close()

            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [CLIENT] - Logged out.{Style.RESET_ALL}")
            sys.exit()

    @commands.command()
    async def reload(self, ctx):
        if self.bot.ownercheck(ctx.author.id):
            for i in os.listdir("cogs"):
                if os.path.isfile(os.path.join("cogs", i)):
                    if f'cogs.{i[:-3]}' in self.bot.extensions:
                        self.bot.unload_extension(f'cogs.{i[:-3]}')
                    else:
                        print(f'{Fore.YELLOW}[{datetime.now()}] [W] [RELOAD] - Is cogs.{i[:-3]} loaded?!{Style.RESET_ALL}')
                    self.bot.load_extension(f'cogs.{i[:-3]}')
            await ctx.reply('Bot Reloaded!')
            print(f'{Fore.LIGHTYELLOW_EX}[{datetime.now()}] [I] [RELOAD] - Reloaded by {ctx.author}.{Style.RESET_ALL}')
    
    @ping.error
    async def on_ping_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            lang = self.check_lang(ctx.guild)
            if lang == "RU":
                emb = disnake.Embed(
                    title='Вы заморожены!',
                    description=f'Попробуйте выполнить команду примерно через {int(error.retry_after)} секунд(у)!',
                    color=0xff0000
                )
            elif lang == "EN":
                emb = disnake.Embed(
                    title='You are on Cooldown!',
                    description=f'Try again in about {int(error.retry_after)} second(s)!',
                    color=0xff0000
                )
            emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=emb)

def setup(bot):
    bot.add_cog(Utils(bot))