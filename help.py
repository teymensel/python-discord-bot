from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Çevre değişkenlerinden prefix bilgisini al
PREFIX = os.getenv('PREFIX', '!')

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Yardım", description="Bot komutları:", color=discord.Color.red())
        prefix = PREFIX

        for cog, commands_list in mapping.items():
            if cog is None:
                cog_name = "Kategori Yok"
            else:
                cog_name = cog.qualified_name

            command_list = [f"`{prefix}{command.name}` - {command.short_doc}" for command in commands_list if command]
            if command_list:
                embed.add_field(name=cog_name, value="\n".join(command_list), inline=False)
        
        embed.set_footer(text=f"Bir komut hakkında daha fazla bilgi için {prefix}help <komut> yazabilirsiniz.")
        channel = self.get_destination()
        await channel.send(embed=embed)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.help_command = CustomHelpCommand()

async def setup(bot):
    await bot.add_cog(Help(bot))
