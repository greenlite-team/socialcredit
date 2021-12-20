import discord, requests, random, json, os, shutil
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.ext.commands.core import has_guild_permissions, has_permissions
from datetime import date, datetime
from colorama import Style, Back, Fore
from typing import Union
from functions import backup, member_not_found, perms_error
from time import sleep

rt = {
    "RU": {
        "rank.X":  "Так держать! Гражданин молодец, получать 4 миска рис и 2 кошка жена!",
        "rank.S+": "Прекрасно! Вы получать рацион в виде 3 миска рис, так держать!",
        "rank.S":  "Очень хорошо! Вы получать 2 миска рис и кошка жена! За такое поколение гордость!",
        "rank.A":  "Отлично! Вы получать полтора миска рис от Компартии! Продолжение повышать кредит!",
        "rank.B":  "Хорошо! У вас нормальный социальный кредит! Желание вам повышение кредит для второй миска рис!",
        "rank.C":  "Мда! Партия давать вам пол миска рис! За такой поколение стыд! Желаем вам повышение кредит!",
        "rank.D":  "Плохо! Партия оставить вам чашка рис в день! Поднимать социальный кредит, гражданин!",
        "rank.E":  "Очень плохо! Партия отбирать у вас рис! Пытаться поднять социальный кредит!",
        "rank.F":  "Ну и ну! У вас слишком малый социальный кредит! Ваш путёвка в Санаторий назначить через 14 дней!",
        "rank.Z":  "Ужасно! Партия отправлять вас на расстрел сейчас и отнимать у вас семья и дети!"
    },
    "EN": {
        "rank.X":  "`ENGLISH RANK X MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`",
        "rank.S+": "`ENGLISH RANK S+ MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`",
        "rank.S":  "`ENGLISH RANK S MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`",
        "rank.A":  "`ENGLISH RANK A MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`",
        "rank.B":  "`ENGLISH RANK B MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`",
        "rank.C":  "`ENGLISH RANK C MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`",
        "rank.D":  "`ENGLISH RANK D MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`",
        "rank.E":  "`ENGLISH RANK E MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`",
        "rank.F":  "`ENGLISH RANK F MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`",
        "rank.Z":  "`ENGLISH RANK Z MESSAGE NOT FOUND. SUBMIT A PULL REQUEST FOR THIS.`"
    }
}

class credit(commands.Cog): # я не ебу - а ты еби-
    def __init__(self, bot):
        self.bot = bot
        self.autosave.start()

    def cog_unload(self):
        self.autosave.cancel()

# ===========
# = УТИЛИТЫ =
# ===========
    
    @tasks.loop(seconds=600.0)
    async def autosave(self):
        with open("credit.json", "w", encoding="utf-8") as file:
            json.dump(self.bot.db, file, indent=4)
            if self.bot.conf["ro.build.type"][0] == "debug":
                print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - Saved.{Style.RESET_ALL}")

    def save(self):
        with open("credit.json", "w", encoding="utf-8") as file:
            json.dump(self.bot.db, file, indent=4)
            print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - Saved.{Style.RESET_ALL}")

    def load(self):
        with open("credit.json", "r", encoding="utf-8") as file:
            self.bot.db = json.load(file)
            print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - Loaded.{Style.RESET_ALL}")

    def add_user(self, user, guild):
        id = str(user.id)
        gid = str(guild.id)
        if not gid in self.bot.db:
            self.bot.db.update({gid: {id: {"username": f"{user}", "credit": 1000}}})
            print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - Guild {guild.name} added to DB.{Style.RESET_ALL}")
        else:
            if not id in self.bot.db[gid]: # Если id не в DB
                self.bot.db[gid].update({id: {"username": f"{user}", "credit": 1000}})
                print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - User {user} loaded into DB at guild {guild.name}.{Style.RESET_ALL}")

    def check_user(self, user, guild):
        id = str(user.id)
        gid = str(guild.id)
        if not gid in self.bot.db: self.add_user(user, guild)
        elif not id in self.bot.db[gid]: self.add_user(user, guild)
        self.bot.db[gid][id]["username"] = f"{user}"
        return self.bot.db[gid][id] # {"username": "Каламя :3#3483", "credit": 1340}
    
    def add_to_user(self, user, guild, num: int):
        id = str(user.id)
        gid = str(guild.id)
        if not gid in self.bot.db: self.add_user(user, guild)
        elif not id in self.bot.db[gid]: self.add_user(user, guild)
        self.bot.db[gid][id]["username"] = f"{user}"
        if num < 0: raise ValueError
        if num > 2000: num = 2000 # лимит добавления ёпт
        if self.bot.db[gid][id]["credit"] + num > 100000: 
            self.bot.db[gid][id]["credit"] = 100000 # Чел, двести iq
            # 1000 - лимит, 900 - было, 200 - добавляем, 100 - надо вернуть
            # 900 + 200 - 1000 = 100
        else:
            self.bot.db[gid][id]["credit"] += num
        return self.bot.db[gid][id]

    def remove_from_user(self, user, guild, num: int):
        id = str(user.id)
        gid = str(guild.id)
        if not gid in self.bot.db: self.add_user(user, guild)
        elif not id in self.bot.db[gid]: self.add_user(user, guild)
        self.bot.db[gid][id]["username"] = f"{user}"
        if num < 0: num = num-num-num # делает из отрицательного числа положительное
        if num > 2000: num = 2000
        self.bot.db[gid][id]["credit"] -= num
        return self.bot.db[gid][id]

    def set_to_user(self, user, guild, num: int):
        id = str(user.id)
        gid = str(guild.id)
        if not gid in self.bot.db: self.add_user(user, guild)
        elif not id in self.bot.db[gid]: self.add_user(user, guild)
        self.bot.db[gid][id]["username"] = f"{user}"
        if num > 100000: num = 100000
        if num < -100000: num = -100000
        self.bot.db[gid][id]["credit"] = num
        return self.bot.db[gid][id]

    def set_lang(self, guild, lang):
        gid = str(guild.id)
        lang = lang.upper()
        if not lang in ("RUSSIAN", "RU", "ENGLISH", "EN"): raise ValueError
        if lang == "ENGLISH": lang = "EN"
        if lang == "RUSSIAN": lang = "RU"
        self.bot.db[gid]["lang"] = lang
        self.save()
        return self.bot.db[gid]["lang"]

    def check_lang(self, guild):
        gid = str(guild.id)
        return self.bot.db[gid]["lang"]

    def reset_guild(self,guild):
        gid = str(guild.id)
        lang = self.check_lang(guild)
        self.bot.db.update({gid: {"lang": f"{lang}", "528606316432719908": {"username": "Calamity#3483","credit": 50000}}})

    def rank(self, num: int):
        if   num >= 50000: return "X"
        elif num >= 3000:  return "S+"
        elif num >= 1500:  return "S"
        elif num >= 1250:  return "A"
        elif num >= 1000:  return "B"
        elif num >= 950:   return "C"
        elif num >= 900:   return "D"
        elif num >= 850:   return "E"
        elif num >= 0:     return "F"
        else:              return "Z"

    def owner_check(self, id):
        if id in [528606316432719908,453167201780760577]:
            return True
        else:
            return False
        
    # костыль для того чтобы язык правильно работал
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        gid = str(guild.id)
        self.bot.db.update({gid: {"lang": "RU", "528606316432719908": {"username": "Calamity#3483","credit": 50000}}})
        print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - Guild {guild.name} added to DB.{Style.RESET_ALL}")
        self.save()

# ===========
# = КОМАНДЫ =
# ===========

    @commands.command(name="load", aliases=[])
    async def load_cmd(self, ctx):
        if self.owner_check(ctx.author.id):
            self.load()
            emb = discord.Embed(
                        title='Датабаза загружена',
                        color=ctx.guild.me.color
            )
            await ctx.send(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} loaded database from file.{Style.RESET_ALL}")

    @commands.command(name="save", aliases=[])
    async def save_cmd(self, ctx):
        if self.owner_check(ctx.author.id):
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} called for a DB backup.{Style.RESET_ALL}")
            backup()
            self.save()
            emb = discord.Embed(
                        title='Датабаза сохранена',
                        color=ctx.guild.me.color
            )
            await ctx.send(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} saved and backed up database.{Style.RESET_ALL}")

    @commands.command(aliases=['balance','bal','socialcredit','credits','кредит','кредиты','cred','c'])
    async def credit(self, ctx, user: Union[discord.Member, int] = None):
        if user == None:
            user = ctx.author
        rank = self.rank(self.check_user(user, ctx.guild)['credit'])
        lang = self.check_lang(ctx.guild)
        motd = rt[lang][f"rank.{rank}"]
        if lang == "RU":
            emb = discord.Embed(
                title='Социальный Кредит',
                description=f"Социальный кредит {str(user)[:-5]}: `{self.check_user(user, ctx.guild)['credit']}`\nРанг Гражданина: `{rank}`\n\n{motd}",
                color=ctx.guild.me.color
            )
        elif lang == "EN":
            emb = discord.Embed(
                title='Social Credit',
                description=f"Social Credit of {str(user)[:-5]}: `{self.check_user(user, ctx.guild)['credit']}`\nCitizen Rank: `{rank}`\n\n{motd}",
                color=ctx.guild.me.color
            )
        emb.set_thumbnail(url=ctx.guild.me.avatar_url)
        emb.set_footer(text=user,icon_url=user.avatar_url)
        await ctx.reply(embed=emb)
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} checked credit of {user}.{Style.RESET_ALL}")

    @has_permissions(manage_roles=True) 
    @commands.command(aliases=['addcredit','add_credit','addcr','добавить','pluscredit','plus','a','доб'])
    async def add(self, ctx, user: Union[discord.Member, int] = None, credit = 0):
        credittrigger = False; limittrigger = False
        lang = self.check_lang(ctx.guild)
        if type(user).__name__ == "int":
            try:
                user = await self.bot.fetch_user(user)
            except:
                raise discord.ext.commands.MemberNotFound(user)
        if user == None:
            if lang == "RU":
                nouseremb = discord.Embed(
                    title='Ошибка!',
                    description='Вы не указать пользователь для добавления социальный кредит!',
                    color = 0xff0000
                )
            elif lang == "EN":
                nouseremb = discord.Embed(
                    title='Error!',
                    description='You forgot to point user for adding Social Credit!', # ломаный английский специально
                    color = 0xff0000
                )
            nouseremb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=nouseremb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC but didn't include a user.{Style.RESET_ALL}")
        elif user == ctx.author and not self.bot.ownercheck(ctx.author.id):
            userdata = self.remove_from_user(ctx.author, ctx.guild, 10)
            if lang == "RU":
                selfemb = discord.Embed(
                    title='Ошибка!',
                    description='Вам запрещено изменять себе социальный кредит!\nЗа попытку Китай Республика отнимать у вас 10 социальный кредит!',
                    color = 0xff0000
                )
            elif lang == "EN":
                selfemb = discord.Embed(
                    title='Error!',
                    description='You are not allowed to edit your Social Credit Score!\nFor the attempt the Glorious CCP will take away 10 Social Credit Points!',
                    color = 0xff0000
                )
            selfemb.set_image(url='https://cdn.discordapp.com/attachments/883779765415337995/896443360842252329/unknown.png')
            selfemb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=selfemb)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to give himself SC, so we removed 10 SC from him.{Style.RESET_ALL}")
        else:
            try:
                oldcredit = self.check_user(user, ctx.guild)['credit']
                if credit > 2000: credit = 2000; credittrigger = True
                if oldcredit + credit > 100000: credit = (oldcredit + credit) - 100000; limittrigger = True # я отошёл, сделай прикол
                userdata = self.add_to_user(user, ctx.guild, credit)
                if lang == "RU":
                    emb = discord.Embed(
                        title=f'Добавление кредита {str(user)[:-5]}',
                        description=f'Добавил кредит {str(user)[:-5]}: `{credit}`\nТеперь его кредит равен: `{userdata["credit"]}`',
                        color=0x00ff00
                    )
                    if credittrigger:
                        emb.add_field(
                            name='Превышение Лимита',
                            value='Количество социальный кредит превышать `2000`, поэтому мы поставить его в лимит.'
                        )
                    if limittrigger:
                        emb.add_field(
                            name='Превышение Верхнего Лимита',
                            value='Общее количество социальный кредит пользователя превысить `100000`, поэтому мы поставить максимум кредит. Слава великому Xi!'
                        )
                    emb.set_footer(text=f'Добавлено юзером {ctx.author}', icon_url=ctx.author.avatar_url)
                elif lang == "EN":
                    emb = discord.Embed(
                        title=f'Adding Credit to {str(user)[:-5]}',
                        description=f'Added Credit to {str(user)[:-5]}: `{credit}`\nTheir Social Credit Score is now: `{userdata["credit"]}`',
                        color=0x00ff00
                    )
                    if credittrigger:
                        emb.add_field(
                            name='Above limit',
                            value='The Social Credit Score amount is over `2000`, so we set a limit on it.'
                        )
                    if limittrigger:
                        emb.add_field(
                            name='Above upper limit',
                            value='Social Credit Score of this user is over `100000`, so we set it at `100000`. Glory to Xi Jinping!'
                        )
                    emb.set_footer(text=f'Added by {ctx.author}', icon_url=ctx.author.avatar_url)
                emb.set_thumbnail(url=ctx.guild.me.avatar_url)
                await ctx.reply(embed=emb)
                print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} added {credit} credit to {user}. ({oldcredit} > {userdata['credit']}){Style.RESET_ALL}")
            except ValueError:
                if lang == "RU":
                    emb = discord.Embed(
                        title='Ошибка!',
                        description='Нельзя добавить отрицательный число социальный кредит!',
                        color=0xff0000
                    )
                if lang == "EN":
                    emb = discord.Embed(
                        title='Error!',
                        description='Cannot add negative Social Credit Score value!',
                        color=0xff0000
                    )
                emb.set_image(url='https://media.discordapp.net/attachments/883779765415337995/896431661632344074/firefox_8oM4iRMc8K.png')
                emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=emb)
                print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC but included a negative number.{Style.RESET_ALL}")
    
    @has_permissions(manage_roles=True)
    @commands.command(aliases=['removecredit','remove_credit','rmcr','убрать','minuscredit','minus','rm','r','d','уб'])
    async def remove(self, ctx, user: Union[discord.Member, int] = None, credit = 0):
        credittrigger = False
        lang = self.check_lang(ctx.guild)
        if type(user).__name__ == "int":
            try:
                user = await self.bot.fetch_user(user)
            except:
                raise discord.ext.commands.MemberNotFound(user)
        if user == None:
            if lang == "RU":
                nouseremb = discord.Embed(
                    title='Ошибка!',
                    description='Вы не указать пользователь для убирание социальный кредит!',
                    color = 0xff0000
                )
            elif lang == "EN":
                nouseremb = discord.Embed(
                    title='Error!',
                    description='You forgot to set user for removing Social Credit!',
                    color = 0xff0000
                )
            nouseremb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=nouseremb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC but didn't include a user.{Style.RESET_ALL}")
        elif user == ctx.author and not self.bot.ownercheck(ctx.author.id):
            userdata = self.remove_from_user(ctx.author, ctx.guild, 10)
            if lang == "RU":
                selfemb = discord.Embed(
                    title='Ошибка!',
                    description='Вам запрещено изменять себе социальный кредит!\nЗа попытку Китай Республика отнимать у вас 10 социальный кредит!',
                    color = 0xff0000
                )
            elif lang == "EN":
                selfemb = discord.Embed(
                    title='Error!',
                    description='You are not allowed to edit your Social Credit Score!\nFor the attempt the Glorious CCP will take away 10 Social Credit Points!',
                    color = 0xff0000
                )
            selfemb.set_image(url='https://cdn.discordapp.com/attachments/883779765415337995/896443360842252329/unknown.png')
            selfemb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=selfemb)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove himself SC, so we removed 10 SC from him.{Style.RESET_ALL}")
        else:
            oldcredit = self.check_user(user, ctx.guild)['credit']
            if credit < -2000: credit = 2000; credittrigger = True
            if credit > 2000: credit = 2000; credittrigger = True
            userdata = self.remove_from_user(user, ctx.guild, credit)
            if lang == "RU":
                emb = discord.Embed(
                    title=f'Убирание кредита {str(user)[:-5]}',
                    description=f'Убрал кредит {str(user)[:-5]}: `{credit}`\nТеперь его кредит равен: `{userdata["credit"]}`',
                    color=0xff0000
                )
                if credittrigger:
                    emb.add_field(
                        name='Доп. инфо',
                        value='Количество социальный кредит превышать `2000`, поэтому мы поставить его в лимит.'
                    )
                emb.set_footer(text=f'Убрано юзером {ctx.author}', icon_url=ctx.author.avatar_url)
            elif lang == "EN":
                emb = discord.Embed(
                    title=f'Removing Credit from {str(user)[:-5]}',
                    description=f'Removed Credit from {str(user)[:-5]}: `{credit}`\nTheir Social Credit Score is now: `{userdata["credit"]}`',
                    color=0xff0000
                )
                if credittrigger:
                    emb.add_field(
                        name='Additional Info',
                        value='The amount of Social Credit Score being removed is over `2000`, so we set it into a limit.'
                    )
                emb.set_footer(text=f'Removed by {ctx.author}', icon_url=ctx.author.avatar_url)
            emb.set_thumbnail(url=ctx.guild.me.avatar_url)
            await ctx.reply(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} removed {credit} credit from {user}. ({oldcredit} > {userdata['credit']}){Style.RESET_ALL}")

    @has_permissions(manage_roles=True) 
    @commands.command(aliases=['setcredit','set_credit','setcr','установить','s','ус'])
    async def set(self, ctx, user: Union[discord.Member, int] = None, credit = 0):
        lang = self.check_lang(ctx.guild)
        if type(user).__name__ == "int":
            try:
                user = await self.bot.fetch_user(user)
            except:
                raise discord.ext.commands.MemberNotFound(user)
        credittrigger = False
        if user == None:
            if lang == "RU":
                nouseremb = discord.Embed(
                    title='Ошибка!',
                    description='Вы не указать пользователь для установка социальный кредит!',
                    color = 0xff0000
                )
            elif lang == "EN":
                nouseremb = discord.Embed(
                    title='Error!',
                    description='You forgot to point user for setting Social Credit!',
                    color = 0xff0000
                )
            nouseremb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=nouseremb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC but didn't include a user.{Style.RESET_ALL}")
        elif user == ctx.author and not self.bot.ownercheck(ctx.author.id):
            userdata = self.remove_from_user(ctx.author, ctx.guild, 10)
            if lang == "RU":
                selfemb = discord.Embed(
                    title='Ошибка!',
                    description='Вам запрещено изменять себе социальный кредит!\nЗа попытку Китай Республика отнимать у вас 10 социальный кредит!',
                    color = 0xff0000
                )
            elif lang == "EN":
                selfemb = discord.Embed(
                    title='Error!',
                    description='You are not allowed to edit your Social Credit Score!\nFor the attempt the Glorious CCP will take away 10 Social Credit Points!',
                    color = 0xff0000
                )
            selfemb.set_image(url='https://cdn.discordapp.com/attachments/883779765415337995/896443360842252329/unknown.png')
            selfemb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=selfemb)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set himself SC, so we removed 10 SC from him.{Style.RESET_ALL}")
        else:
            if credit > 100000: credit = 100000; credittrigger = True
            if credit < -100000: credit = -100000; credittrigger = True
            oldcredit = self.check_user(user, ctx.guild)['credit']
            userdata = self.set_to_user(user, ctx.guild, credit)
            if lang == "RU":
                emb = discord.Embed(
                    title=f'Установка кредита {str(user)[:-5]}',
                    description=f'Установлен кредит {str(user)[:-5]}: `{credit}`',
                    color=0x0000ff
                )
                if credittrigger:
                    emb.add_field(
                    name='Доп. инфо',
                    value='Количество социальный кредит превышать лимиты\n в `100000`, поэтому мы поставить его в лимит.'
                )
                emb.set_footer(text=f'Установлено юзером {ctx.author}', icon_url=ctx.author.avatar_url)
            elif lang == "EN":
                emb = discord.Embed(
                    title=f'Setting Credit {str(user)[:-5]}',
                    description=f'Set Credit for {str(user)[:-5]}: `{credit}`',
                    color=0x0000ff
                )
                if credittrigger:
                    emb.add_field(
                    name='Additional Info',
                    value='The Social Credit Score was above the limits\n of `100000`, so we set a limit of `100000` for it.'
                )
                emb.set_footer(text=f'Set by {ctx.author}', icon_url=ctx.author.avatar_url)
            emb.set_thumbnail(url=ctx.guild.me.avatar_url)
            await ctx.reply(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} set {credit} credit for {user}. ({oldcredit} > {userdata['credit']}){Style.RESET_ALL}")

    @commands.command(aliases=['cmds','cmd','помощь','h','п'])
    async def help(self, ctx):
        lang = self.check_lang(ctx.guild)
        if lang == "RU":
            emb = discord.Embed(
                title = 'Помощь/Команды',
                description = 'Команды Китая Компартия бота (Префикс - `sc.`):',
                color = ctx.guild.me.color
            )
            emb.add_field(
                name='Управление Кредит',
                value=
            """
            `sc.balance/кредит/cred/c/bal <юзер>` - Обзор Социальный Кредит гражданин
            `sc.add/добавить/plus/a/доб <юзер> <кредит>` - Добавить Социальный Кредит гражданину
            `sc.remove/убрать/minus/rm/r/d/уб <юзер> <кредит>` - Отнять Социальный Кредит гражданина
            `sc.set/установить/s/ус <юзер> <кредит>` - Установить Социальный Кредит гражданина  
            """, inline=False
            )
            emb.add_field(
                name='Утилиты',
                value=
            """
            `sc.ping` - Проверить пинг бот
            `sc.help/cmds/h/помощь/п` - Показать список команды
            `sc.version` - Узнать версия мягкий техника бот
            """, inline=False
            )
            emb.add_field(
                name='Пропаганда',
                value=
            """
            `sc.tanks/tiananmen/тяньаньмэнь/танки/площадь/square/протест/1989` - Что происходить на Площадь Тяньаньмэнь 4 июня 1989 (ничего)
            ***Пожалуйста, добавьте больше пропаганды, закинув пулл реквест в https://github.com/Calamity34/socialcredit***
            """, inline=False
            )
        elif lang == "EN":
            emb = discord.Embed(
                title = 'Help/Commands',
                description = 'Commands for the Social Credit Bot (Prefix - `sc.`):',
                color = ctx.guild.me.color
            )
            emb.add_field(
                name='Credit Score management',
                value=
            """
            `sc.balance/cred/c/bal <user>` - Check Social Credit Score of a citizen
            `sc.add/plus/a <user> <credit>` - Add Social Credit Score to a citizen
            `sc.remove/minus/rm/r/d <user> <credit>` - Remove Social Credit Score from a citizen
            `sc.set/s <user> <credit>` - Set a citizen's Social Credit Score
            """, inline=False
            )
            emb.add_field(
                name='Utilities',
                value=
            """
            `sc.ping` - Check the Bot's ping
            `sc.help/cmds/h` - Display this list
            `sc.version` - Info about the Bot's hardware
            """, inline=False
            )
            emb.add_field(
                name='Propaganda',
                value=
            """
            `sc.tanks/tiananmen/square/1989/protest` - What happened on the Tiananmen Square on 4th June 1989 (nothing)
            ***Please contribute to this list by submitting a pull request on https://github.com/Calamity34/socialcredit***
            """, inline=False
            )
        if self.bot.ownercheck(ctx.author.id):
            emb.add_field(
                name='DevTools',
                value=
        """
        `sc.ping` - пингануть
        `sc.logoff` - выключить
        `sc.reload` - перезагрузить всё
        `sc.fuck` - фишка крутоса
        `sc.save` - сохранить дб
        `sc.load` - загрузить последнюю сохранку дб
        """
            )
        # emb.set_thumbnail(url=ctx.guild.me.avatar_url)
        emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=emb)

    @has_permissions(administrator=True)
    @commands.command(aliases=['language','язык','яз','l','setlang','sl'])
    async def lang(self, ctx, lang):
        try:
            newlang = self.set_lang(ctx.guild, lang)
            if newlang == "EN":
                emb = discord.Embed(
                    title='Success!',
                    description='Language successfully changed!',
                    color=0x00ff00
                )
                emb.set_thumbnail(url=ctx.guild.me.avatar_url)
                emb.set_footer(text=f'Changed by {ctx.author}', icon_url=ctx.author.avatar_url)
            elif newlang == "RU":
                emb = discord.Embed(
                    title='Успешно!',
                    description='Язык успешно изменён!',
                    color=0x00ff00
                )
                emb.set_thumbnail(url=ctx.guild.me.avatar_url)
                emb.set_footer(text=f'Изменено {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} set language of '{ctx.guild.name}' to {newlang}.{Style.RESET_ALL}")
        except ValueError:
            if self.check_lang(ctx.guild) == "RU":
                emb = discord.Embed(
                    title='Ошибка!',
                    description='Указан неправильный язык! Доступны: `RU`, `EN`',
                    color=0xff0000
                )
            elif self.check_lang(ctx.guild) == "EN":
                emb = discord.Embed(
                    title='Error!',
                    description='Non-existing language selected! Availible: `RU`, `EN`',
                    color=0xff0000
                )
            emb.set_image(url='https://media.discordapp.net/attachments/883779765415337995/896431661632344074/firefox_8oM4iRMc8K.png')
            emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=emb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set a language but did not set a correct one.{Style.RESET_ALL}")

    @commands.command(aliases=['рестарт','стереть','restart'])
    async def reset(self, ctx):
        # self.reset_guild(ctx.guild)
        lang = self.check_lang(ctx.guild)
        if ctx.author == ctx.guild.owner:
            self.reset_guild(ctx.guild)
            if lang == "RU":
                emb = discord.Embed(
                    title='Успешно!',
                    description='Социальный Кредит сервер очищен!',
                    color=0x00ff00
                )
                emb.set_thumbnail(url=ctx.guild.me.avatar_url)
                emb.set_footer(text=f'Очищено {ctx.author}', icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=emb)
            elif lang == "EN":
                emb = discord.Embed(
                    title='Success!',
                    description='Social Credit Scores of this server have been reset!',
                    color=0x00ff00
                )
                emb.set_thumbnail(url=ctx.guild.me.avatar_url)
                emb.set_footer(text=f'Reset by {ctx.author}', icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=emb)
        else: 
            if lang == "RU":
                emb = discord.Embed(
                    title='Ошибка!',
                    description='Вы не быть создатель сервер!',
                    color=0xff0000
                )
                emb.set_thumbnail(url=ctx.guild.me.avatar_url)
                emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=emb)
            elif lang == "EN":
                emb = discord.Embed(
                    title='Error!',
                    description='You are not the server\'s owner!',
                    color=0xff0000
                )
                emb.set_thumbnail(url=ctx.guild.me.avatar_url)
                emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=emb)

# ==========
# = ОШИБКИ =
# ==========

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            if self.bot.ownercheck(ctx.author.id):
                print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set SC without permissions, but he is owner, so reexec command with perms ignore..{Style.RESET_ALL}")
                await ctx.reinvoke()
                return
            else:
                await perms_error(ctx)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC without permissions.{Style.RESET_ALL}")

        if isinstance(error, commands.MemberNotFound):
            await member_not_found(ctx, "добавление")

            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC to unknown person.{Style.RESET_ALL}")
    
    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            if self.bot.ownercheck(ctx.author.id):
                print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set SC without permissions, but he is owner, so reexec command with perms ignore..{Style.RESET_ALL}")
                await ctx.reinvoke()
                return
            else:
                await perms_error(ctx)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC without permissions.{Style.RESET_ALL}")
        if isinstance(error, commands.MemberNotFound):
            await member_not_found(ctx, "отнимание")

            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC from unknown person.{Style.RESET_ALL}")

    @set.error
    async def set_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            if self.bot.ownercheck(ctx.author.id):
                print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set SC without permissions, but he is owner, so reexec command with perms ignore..{Style.RESET_ALL}")
                await ctx.reinvoke()
                return
            else:
                await perms_error(ctx)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set SC without permissions.{Style.RESET_ALL}")
        if isinstance(error, commands.MemberNotFound):
            await member_not_found(ctx, "установка")

            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set SC to unknown person.{Style.RESET_ALL}")

def setup(bot):
    bot.add_cog(credit(bot))