import disnake, json
from disnake.ext import commands
from datetime import datetime
from colorama import Back, Fore, Style

class kek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load(self):
        with open("credit.json", "r", encoding="utf-8") as file:
            self.bot.db = json.load(file)

    def check_lang(self, guild):
        self.load()
        gid = str(guild.id)
        return self.bot.db[gid]["lang"]

    @commands.command(aliases=['tiananmen','тяньаньмэнь','тианамен','танки','площадь','square','протест','1989','тяньмэнь','тиананмен','protest']) 
    async def tanks(self, ctx):
        lang = self.check_lang(ctx.guild)
        if lang == "RU":
            emb = disnake.Embed(
                title='Ничего не происходить в 1989 на Площади Тяньаньмэнь!',
                color = ctx.guild.me.color
            ) # ничего не происходить в комментарий строка 27 файл kek.py
        elif lang == "EN":
            emb = disnake.Embed(
                title='Nothing happened in 1989 on the Tiananmen Square!',
                color = ctx.guild.me.color
            )
        emb.set_image(url='https://media.discordapp.net/attachments/883778578318258222/897894172915294239/unknown.png')
        emb.set_footer(text=ctx.author,icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=emb)

def setup(bot):
    bot.add_cog(kek(bot))