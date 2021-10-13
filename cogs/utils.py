import discord, colorama, sys, os
from datetime import datetime
from colorama import Back, Fore, Style
from discord.embeds import Embed
from discord.ext import commands, tasks
from functions import backup

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"{Fore.LIGHTGREEN_EX}[{datetime.now()}] [I] [+GUILD] - Bot joined a new guild: '{guild.name}'. Member count: '{guild.member_count}'.{Style.RESET_ALL}")
        emb = discord.Embed(
            title='Спасибо за добавление!',
            description="Я есть Социальный Кредит бот разработанный `Calamity#3483` и `KrutosX#3599` совместно с Коммунистическая Партия Китай.",
            color=guild.me.color
        )
        emb.add_field(
            name="Что я уметь?",
            value="Данный бот уметь добавление/отнимание/установка Социальный Кредит, и Китай Пропаганда (молчание!).\nУзнать больше: `sc.help`",
            inline=False
        )
        for i in guild.text_channels:
            perm = i.permissions_for(guild.me)
            if perm.send_messages:
                await i.send(embed=emb)
                break

    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        print(f"{Fore.LIGHTGREEN_EX}[{datetime.now()}] [I] [-GUILD] - Bot leaved guild: '{guild.name}'. Member count: '{guild.member_count}'.{Style.RESET_ALL}")
    
    @commands.cooldown(rate=1, per=10)
    @commands.command()
    async def ping(self, ctx):
        emb = discord.Embed(
            title='Понг!',
            description=f'Пинг: {int(round(self.bot.latency, 4) * 1000)}',
            color=ctx.guild.me.color
        )
        await ctx.reply(embed=emb)
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - 'ping' command executed by {ctx.author}.{Style.RESET_ALL}")

    @commands.command()
    async def version(self, ctx):
        emb = discord.Embed(
            title='Версии',
            description=f'Версия: `{self.bot.conf["ro.bot.version"]}`\nВерсия Python: `{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}`\nВерсия discord.py: `{discord.__version__}`',
            color=0xff0000
        )
        await ctx.reply(embed=emb)
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - 'version' command executed by {ctx.author}.{Style.RESET_ALL}")

    @commands.command(aliases=["quit", 'logout', 'выйти', 'выключить', 'вырубить', 'poweroff'])
    async def logoff(self, ctx):
        if self.bot.ownercheck(ctx.author.id):
            await ctx.reply("Выключаюсь...")
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
            await ctx.send('Бот перезагружен!')
            print(f'{Fore.LIGHTYELLOW_EX}[{datetime.now()}] [I] [RELOAD] - Reloaded by {ctx.author}.{Style.RESET_ALL}')
    
    @ping.error
    async def on_ping_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            emb = discord.Embed(
                title='Вы заморожены!',
                description=f'Попробуйте выполнить команду примерно через {int(error.retry_after)} секунд!',
                color=0xff0000
            )
            emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)

            await ctx.reply(embed=emb)

def setup(bot):
    bot.add_cog(Utils(bot))