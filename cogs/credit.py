import discord, requests, random, json, os, shutil
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.ext.commands.core import has_guild_permissions, has_permissions
from datetime import date, datetime
from colorama import Style, Back, Fore

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
        if num < 0:
            raise ValueError
        self.bot.db[id]["credit"] += num
        return self.bot.db[id]

    def remove_from_user(self, user, num: int):
        id = str(user.id)
        if not id in self.bot.db: self.add_user(user)
        self.bot.db[id]["username"] = f"{user.name}#{user.discriminator}"
        if num < 0:
            num = num-num-num # делает из отрицательного числа положительное
        self.bot.db[id]["credit"] -= num
        return self.bot.db[id]

    def set_to_user(self, user, num: int):
        id = str(user.id)
        if not id in self.bot.db: self.add_user(user)
        self.bot.db[id]["username"] = f"{user.name}#{user.discriminator}"
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

    @commands.command(aliases=['balance','socialcredit','credits','кредит','кредиты'])
    async def credit(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        emb = discord.Embed(
            title='Социальный Кредит',
            description=f"> {self.check_user(user)['credit']}",
            color=ctx.guild.me.color
        )
        emb.set_thumbnail(url=ctx.guild.me.avatar_url)
        emb.set_footer(text=user,icon_url=user.avatar_url)
        await ctx.send(embed=emb)
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} checked credit of {user}.{Style.RESET_ALL}")

    @has_permissions(manage_roles=True) 
    @commands.command(aliases=['addcredit','add_credit','addcr','добавить','pluscredit','plus'])
    async def add(self, ctx, user: discord.Member = None, credit = 0): 
        if user == None:
            nouseremb = discord.Embed(
                title='Ошибка!',
                description='Вы не указать пользователь для добавления социальный кредит!',
                color = 0xff0000
            )
            nouseremb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=nouseremb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC but didn't include a user.{Style.RESET_ALL}")
        elif user == ctx.author:
            userdata = self.remove_from_user(ctx.author, 10)
            selfemb = discord.Embed(
                title='Ошибка!',
                description='Вам запрещено изменять себе социальный кредит!\nЗа попытку Китай Республика отнимать у вас 10 социальный кредит!',
                color = 0xff0000
            )
            selfemb.set_image(url='https://cdn.discordapp.com/attachments/883779765415337995/896443360842252329/unknown.png')
            selfemb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=selfemb)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to give himself SC, so we removed 10 SC from him.{Style.RESET_ALL}")
        else:
            oldcredit = self.check_user(user)['credit']
            try:
                userdata = self.add_to_user(user, credit)
                emb = discord.Embed(
                    title=f'Добавление кредита {str(user)[:-5]}',
                    description=f'Добавил кредит {str(user)[:-5]}: `{credit}`\nТеперь его кредит равен: `{userdata["credit"]}`',
                    color=0x00ff00
                )
                emb.set_thumbnail(url=ctx.guild.me.avatar_url)
                emb.set_footer(text=f'Добавлено юзером {ctx.author}', icon_url=ctx.author.avatar_url)
                await ctx.send(embed=emb)
                print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} added {credit} credit to {user}. ({oldcredit} > {userdata['credit']}){Style.RESET_ALL}")
            except ValueError:
                emb = discord.Embed(
                    title='Ошибка!',
                    description='Нельзя добавить отрицательный число социальный кредит!',
                    color=0xff0000
                )
                emb.set_image(url='https://media.discordapp.net/attachments/883779765415337995/896431661632344074/firefox_8oM4iRMc8K.png')
                emb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=emb)
                print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC but included a negative number.{Style.RESET_ALL}")

    @commands.command(aliases=['removecredit','remove_credit','rmcr','убрать','minuscredit','minus','rm'])
    @has_permissions(manage_roles=True)
    async def remove(self, ctx, user: discord.Member = None, credit = 0): 
        if user == None:
            nouseremb = discord.Embed(
                title='Ошибка!',
                description='Вы не указать пользователь для убирание социальный кредит!',
                color = 0xff0000
            )
            nouseremb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=nouseremb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC but didn't include a user.{Style.RESET_ALL}")
        elif user == ctx.author:
            userdata = self.remove_from_user(ctx.author, 10)
            selfemb = discord.Embed(
                title='Ошибка!',
                description='Вам запрещено изменять себе социальный кредит!\nЗа попытку Китай Республика отнимать у вас 10 социальный кредит!',
                color = 0xff0000
            )
            selfemb.set_image(url='https://cdn.discordapp.com/attachments/883779765415337995/896443360842252329/unknown.png')
            selfemb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=selfemb)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove himself SC, so we removed 10 SC from him.{Style.RESET_ALL}")
        else:
            oldcredit = self.check_user(user)['credit']
            userdata = self.remove_from_user(user, credit)
            emb = discord.Embed(
                title=f'Убирание кредита {str(user)[:-5]}',
                description=f'Убрал кредит {str(user)[:-5]}: `{credit}`\nТеперь его кредит равен: `{userdata["credit"]}`',
                color=0xff0000
            )
            emb.set_thumbnail(url=ctx.guild.me.avatar_url)
            emb.set_footer(text=f'Убрано юзером {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} removed {credit} credit from {user}. ({oldcredit} > {userdata['credit']}){Style.RESET_ALL}")

    @has_permissions(manage_roles=True) 
    @commands.command(aliases=['setcredit','set_credit','setcr','установить'])
    async def set(self, ctx, user: discord.Member = None, credit = 0): 
        if user == None:
            nouseremb = discord.Embed(
                title='Ошибка!',
                description='Вы не указать пользователь для установка социальный кредит!',
                color = 0xff0000
            )
            nouseremb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=nouseremb)
            print(f"{Fore.LIGHTRED_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC but didn't include a user.{Style.RESET_ALL}")
        elif user == ctx.author:
            userdata = self.remove_from_user(ctx.author, 10)
            selfemb = discord.Embed(
                title='Ошибка!',
                description='Вам запрещено изменять себе социальный кредит!\nЗа попытку Китай Республика отнимать у вас 10 социальный кредит!',
                color = 0xff0000
            )
            selfemb.set_image(url='https://cdn.discordapp.com/attachments/883779765415337995/896443360842252329/unknown.png')
            selfemb.set_footer(text=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=selfemb)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set himself SC, so we removed 10 SC from him.{Style.RESET_ALL}")
        else:
            oldcredit = self.check_user(user)['credit']
            userdata = self.set_to_user(user, credit)
            emb = discord.Embed(
                title=f'Установка кредита {str(user)[:-5]}',
                description=f'Установлен кредит {str(user)[:-5]}: `{credit}`',
                color=0x0000ff
            )
            emb.set_thumbnail(url=ctx.guild.me.avatar_url)
            emb.set_footer(text=f'Установлено юзером {ctx.author}', icon_url=ctx.author.avatar_url)
            await ctx.send(embed=emb)
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [I] [COMMND] - User {ctx.author} set {credit} credit for {user}. ({oldcredit} > {userdata['credit']}){Style.RESET_ALL}")

# ==========
# = ОШИБКИ =
# ==========

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await perms_error(ctx)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC without permissions{Style.RESET_ALL}")

        if isinstance(error, commands.MemberNotFound):
            await member_not_found("добавление")

            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to add SC to unknown person.{Style.RESET_ALL}")
    
    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await perms_error(ctx)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC without permissions{Style.RESET_ALL}")
        if isinstance(error, commands.MemberNotFound):
            await member_not_found("отнимание")

            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to remove SC from unknown person.{Style.RESET_ALL}")

    @set.error
    async def set_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await perms_error(ctx)
            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set SC without permissions{Style.RESET_ALL}")
        if isinstance(error, commands.MemberNotFound):
            await member_not_found("установка")

            print(f"{Fore.LIGHTMAGENTA_EX}[{datetime.now()}] [E] [CMDERR] - User {ctx.author} tried to set SC to unknown person.{Style.RESET_ALL}")

def setup(bot):
    bot.add_cog(credit(bot))