import discord
from discord.ext import commands
from discord.embeds import Embed

from datetime import datetime
from colorama import Back, Fore, Style

class kek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['tiananmen','тяньаньмэнь','тианамен','танки','площадь','square','протест','1989','тяньмэнь','тиананмен','protest']) 
    async def tanks(self, ctx):
        emb = discord.Embed(
            title='Ничего не происходить в 1989 на Площади Тяньаньмэнь!',
            color = ctx.guild.me.color
        ) # ничего не происходить в комментарий строка 17 файл kek.py
        emb.set_image(url='https://media.discordapp.net/attachments/883778578318258222/897894172915294239/unknown.png')
        emb.set_footer(text=ctx.author,icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=emb)

def setup(bot):
    bot.add_cog(kek(bot))