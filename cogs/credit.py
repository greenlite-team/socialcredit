import discord, requests, random, json
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.ext.commands.core import has_guild_permissions, has_permissions
from datetime import date, datetime
from colorama import Style, Back, Fore

class credit(commands.Cog): # я не ебу - а ты еби-
    def __init__(self, bot):
        self.bot = bot
        self.autosave.start()

    def cog_unload(self):
        self.autosave.cancel()
    # =======
    # УТИЛИТЫ
    # =======
    
    @tasks.loop(seconds=600.0)
    async def autosave(self):
        with open("credit.json", "w", encoding="utf-8") as file:
            json.dump(self.bot.db, file, indent=4)
            print(f"{Fore.LIGHTBLUE_EX}[{datetime.now()}] [DATABS] - Saved.{Style.RESET_ALL}")

    def add_user(self, user):
        id = str(user.id)
        if not id in self.bot.db: # Если id не в DB
            self.bot.db.update({id: {"username": f"{user.name}#{user.discriminator}", "credit": 1000}}) 

    def check_user(self, user):
        id = str(user.id)
        if not id in self.bot.db: self.add_user(user)
        self.bot.db[id]["username"] = f"{user.name}#{user.discriminator}"
        return self.bot.db[id] # {"username": "Каламя:3#3483", "credit": 99999999}
        
    # =======
    # КОМАНДЫ 
    # =======
        
    @commands.command(aliases=['balance','socialcredit','credits','кредит','кредиты'])
    async def credit(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        emb = discord.Embed(
            title='Социальный Кредит',
            description=f"> {self.check_user(user)['credit']}",
            color=0xff0000
        )
        emb.set_footer(text=user,icon_url=user.avatar_url)
        await ctx.send(embed=emb)

        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now()}] [COMMND] - User {ctx.author} checked credit of {user}.{Style.RESET_ALL}")


def setup(bot):
    bot.add_cog(credit(bot))