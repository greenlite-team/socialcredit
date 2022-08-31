import disnake
from disnake.ext import commands

class guildlog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        logchannel = await self.bot.fetch_channel(886449232486227998)
        emd = disnake.Embed(
            title=f"Вышел с сервера {guild}",
            description=f"Кол-во участников: **{guild.member_count}**",
            colour=0xff0000
        )
        await logchannel.send(embed=emd)

    @commands.Cog.listener()
    async def on_guild_join(self,guild):
        logchannel = await self.bot.fetch_channel(886449232486227998)
        emd = disnake.Embed(
            title=f"Зашел на сервер {guild}",
            description=f"Кол-во участников: **{guild.member_count}**",
            colour=0x00ff00
        )
        await logchannel.send(embed=emd)
    
def setup(bot):
    bot.add_cog(guildlog(bot))