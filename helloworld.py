from discord.ext import commands

class Greet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def greet(self, ctx):
        await ctx.send("Merhaba Dünya!")

async def setup(bot):
    await bot.add_cog(Greet(bot))
