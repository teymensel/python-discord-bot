import discord
from discord.ext import commands
import re

class RespondBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Botun kendi mesajlarına yanıt vermesin
        if message.author == self.bot.user:
            return

        # Mesajın başında "auuu" var mı kontrol et
        if message.content.lower().startswith("auuu"):
            # Yanıtla
            await message.channel.send("AOUUUUUUUUUUUUU")
        # Ekstra bir işlev, mesajın başında "auuu" içermiyorsa
        elif re.match(r'^[aA][uU]+[sS]*', message.content):
            await message.channel.send("AOUUUUUUUUUUUUU")

async def setup(bot):
    await bot.add_cog(RespondBot(bot))

