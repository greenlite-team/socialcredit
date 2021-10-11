import discord, requests, random, json, os, shutil
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.ext.commands.core import has_guild_permissions, has_permissions
from datetime import date, datetime
from colorama import Style, Back, Fore
from typing import Union
from functions import backup, member_not_found, perms_error

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
            print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - Saved.{Style.RESET_ALL}")

    def save(self):
        with open("credit.json", "w", encoding="utf-8") as file:
            json.dump(self.bot.db, file, indent=4)
            print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [I] [DATABS] - Saved.{Style.RESET_ALL}")

    def add_user(self, user):
        id = str(user.id)
        if not id in self.bot.db: # Если id не в DB
            self.bot.db.update({id: {"username": f"{user.name}#{user.discriminator}", "credit": 1000}}) 

    def check_user(self, user):
        id = str(user.id)
        if not id in self.bot.db: self.add_user(user)
        self.bot.db[id]["username"] = f"{user.name}#{user.discriminator}"
        return self.bot.db[id] # {"username": "Каламя :3#3483", "credit": 1340}
    
    def add_to_user(self, user, num: int):
        id = str(user.id)
        if not id in self.bot.db: self.add_user(user)
        self.bot.db[id]["username"] = f"{user.name}#{user.discriminator}"
        if num < 0: raise ValueError
        if num > 2000: num = 2000 # лимит добавления ёпт
        if self.bot.db[id]["credit"] + num > 100000: 
            self.bot.db[id]["credit"] = 100000 # Чел, двести iq
            # 1000 - лимит, 900 - было, 200 - добавляем, 100 - надо вернуть
            # 900 + 200 - 1000 = 100
        else:
            self.bot.db[id]["credit"] += num
        return self.bot.db[id]

    def remove_from_user(self, user, num: int):
        id = str(user.id)
        if not id in self.bot.db: self.add_user(user)
        self.bot.db[id]["username"] = f"{user.name}#{user.discriminator}"
        if num < 0: num = num-num-num # делает из отрицательного числа положительное
        if num > 2000: num = 2000
        self.bot.db[id]["credit"] -= num
        return self.bot.db[id]

    def set_to_user(self, user, num: int):
        id = str(user.id)
        if not id in self.bot.db: self.add_user(user)
        self.bot.db[id]["username"] = f"{user.name}#{user.discriminator}"
        if num > 100000: num = 100000
        if num < -100000: num = -100000
        self.bot.db[id]["credit"] = num
        return self.bot.db[id]

    def owner_check(self, id):
        if id in [528606316432719908,453167201780760577]:
            return True
        else:
            return False
        
    # ===========
    # = КОМАНДЫ =
    # ===========

    @commands.command(name="save", aliases=[])
    async def save_cmd(self, ctx):
        if self.owner_check(ctx.author.id):
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [COMMND] - User {ctx.author} called for a DB backup.{Style.RESET_ALL}")
            backup()
            self.save()
            emb = discord.Embed(
                        title='Датабаза сохранена',
                        color=ctx.guild.me.color
            )
            await ctx.send(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} saved and backed up database.{Style.RESET_ALL}")

    @commands.command(aliases=[])
    async def fuck(self, ctx):
        emb = discord.Embed(
                    title='Что!?',
                    color=0xff0000
        )
        emb.set_image(url='https://media.discordapp.net/attachments/883779765415337995/896431661632344074/firefox_8oM4iRMc8K.png')
        await ctx.send(embed=emb)

    @commands.command(aliases=['balance','bal','socialcredit','credits','кредит','кредиты','cred','c'])
    async def credit(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        emb = discord.Embed(
            title='Социальный Кредит',
            description=f"Социальный кредит {str(user)[:-5]}: `{self.check_user(user)['credit']}`",
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
        if type(user).__name__ == "int":
            user = await self.bot.fetch_user(user)
        if user == None:
            nouseremb = discord.Embed(
                title='Ошибка!',
                description='Вы не указать пользователь для добавления социальный кредит!',
                color = 0xff0000
            )
            nouseremb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=nouseremb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC but didn't include a user.{Style.RESET_ALL}")
        elif user == ctx.author and not self.bot.ownercheck(ctx.author.id):
            userdata = self.remove_from_user(ctx.author, 10)
            selfemb = discord.Embed(
                title='Ошибка!',
                description='Вам запрещено изменять себе социальный кредит!\nЗа попытку Китай Республика отнимать у вас 10 социальный кредит!',
                color = 0xff0000
            )
            selfemb.set_image(url='https://cdn.discordapp.com/attachments/883779765415337995/896443360842252329/unknown.png')
            selfemb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=selfemb)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to give himself SC, so we removed 10 SC from him.{Style.RESET_ALL}")
        else:
            try:
                oldcredit = self.check_user(user)['credit']
                if credit > 2000: credit = 2000; credittrigger = True
                if oldcredit + credit > 100000: credit = (oldcredit + credit) - 100000; limittrigger = True # я отошёл, сделай прикол
                userdata = self.add_to_user(user, credit)
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
                emb.set_thumbnail(url=ctx.guild.me.avatar_url)
                emb.set_footer(text=f'Добавлено юзером {ctx.author}', icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=emb)
                print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} added {credit} credit to {user}. ({oldcredit} > {userdata['credit']}){Style.RESET_ALL}")
            except ValueError:
                emb = discord.Embed(
                    title='Ошибка!',
                    description='Нельзя добавить отрицательный число социальный кредит!',
                    color=0xff0000
                )
                emb.set_image(url='https://media.discordapp.net/attachments/883779765415337995/896431661632344074/firefox_8oM4iRMc8K.png')
                emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=emb)
                print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC but included a negative number.{Style.RESET_ALL}")

    @commands.command(aliases=['removecredit','remove_credit','rmcr','убрать','minuscredit','minus','rm','r','d','уб'])
    @has_permissions(manage_roles=True)
    async def remove(self, ctx, user: Union[discord.Member, int] = None, credit = 0):
        credittrigger = False
        if type(user).__name__ == "int":
            user = await self.bot.fetch_user(user)
        if user == None:
            nouseremb = discord.Embed(
                title='Ошибка!',
                description='Вы не указать пользователь для убирание социальный кредит!',
                color = 0xff0000
            )
            nouseremb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=nouseremb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC but didn't include a user.{Style.RESET_ALL}")
        elif user == ctx.author and not self.bot.ownercheck(ctx.author.id):
            userdata = self.remove_from_user(ctx.author, 10)
            selfemb = discord.Embed(
                title='Ошибка!',
                description='Вам запрещено изменять себе социальный кредит!\nЗа попытку Китай Республика отнимать у вас 10 социальный кредит!',
                color = 0xff0000
            )
            selfemb.set_image(url='https://cdn.discordapp.com/attachments/883779765415337995/896443360842252329/unknown.png')
            selfemb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=selfemb)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove himself SC, so we removed 10 SC from him.{Style.RESET_ALL}")
        else:
            oldcredit = self.check_user(user)['credit']
            if credit < -2000: credit = 2000; credittrigger = True
            if credit > 2000: credit = 2000; credittrigger = True
            userdata = self.remove_from_user(user, credit)
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
            emb.set_thumbnail(url=ctx.guild.me.avatar_url)
            emb.set_footer(text=f'Убрано юзером {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} removed {credit} credit from {user}. ({oldcredit} > {userdata['credit']}){Style.RESET_ALL}")

    @has_permissions(manage_roles=True) 
    @commands.command(aliases=['setcredit','set_credit','setcr','установить','s','ус'])
    async def set(self, ctx, user: Union[discord.Member, int] = None, credit = 0):
        if type(user).__name__ == "int":
            user = await self.bot.fetch_user(user)
        credittrigger = False
        if user == None:
            nouseremb = discord.Embed(
                title='Ошибка!',
                description='Вы не указать пользователь для установка социальный кредит!',
                color = 0xff0000
            )
            nouseremb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=nouseremb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC but didn't include a user.{Style.RESET_ALL}")
        elif user == ctx.author and not self.bot.ownercheck(ctx.author.id):
            userdata = self.remove_from_user(ctx.author, 10)
            selfemb = discord.Embed(
                title='Ошибка!',
                description='Вам запрещено изменять себе социальный кредит!\nЗа попытку Китай Республика отнимать у вас 10 социальный кредит!',
                color = 0xff0000
            )
            selfemb.set_image(url='https://cdn.discordapp.com/attachments/883779765415337995/896443360842252329/unknown.png')
            selfemb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=selfemb)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set himself SC, so we removed 10 SC from him.{Style.RESET_ALL}")
        else:
            if credit > 100000: credit = 100000; credittrigger = True
            if credit < -100000: credit = -100000; credittrigger = True
            oldcredit = self.check_user(user)['credit']
            userdata = self.set_to_user(user, credit)
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
            emb.set_thumbnail(url=ctx.guild.me.avatar_url)
            emb.set_footer(text=f'Установлено юзером {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} set {credit} credit for {user}. ({oldcredit} > {userdata['credit']}){Style.RESET_ALL}")

# ==========
# = ОШИБКИ =
# ==========

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await perms_error(ctx)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC without permissions.{Style.RESET_ALL}")

        if isinstance(error, commands.MemberNotFound):
            await member_not_found(ctx, "добавление")

            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC to unknown person.{Style.RESET_ALL}")
    
    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await perms_error(ctx)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC without permissions.{Style.RESET_ALL}")
        if isinstance(error, commands.MemberNotFound):
            await member_not_found(ctx, "отнимание")

            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC from unknown person.{Style.RESET_ALL}")

    @set.error
    async def set_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            #if self.bot.ownercheck(ctx.author.id):
            #    await self.bot.invoke(ctx)
            #else:
            await perms_error(ctx)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set SC without permissions.{Style.RESET_ALL}")
        if isinstance(error, commands.MemberNotFound):
            await member_not_found(ctx, "установка")

            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set SC to unknown person.{Style.RESET_ALL}")

def setup(bot):
    bot.add_cog(credit(bot))