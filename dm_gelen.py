import discord
from discord.ext import commands
import requests

WEBHOOK_URL = 'https://discord.com/api/webhooks/1268990513906978897/Sdcj32X0FWOsdQwMlMEb9giKCixt5p6oD_U5M5CKHQjFT52lvdUGSHmEbQgOUoCOUSvu'
ICON_URL = 'https://images-ext-1.discordapp.net/external/sBdwHSdQ2cRf5xgylGELMplL_37L4MYJroFe44_H3NY/https/www.pngmart.com/files/13/Secret-Agent-PNG-File.png?format=webp&quality=lossless&width=634&height=634'

class DMListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Bot kendi mesajlarını kontrol etme
        if message.author == self.bot.user:
            return
        
        # Eğer mesaj DM'den geldiyse
        if isinstance(message.channel, discord.DMChannel):
            # Webhook'a gönderilecek veri
            embed = {
                "embeds": [
                    {
                        "title": "Bota DM'den Yazdı",
                        "color": 0x000000,  # Siyah renk
                        "author": {
                            "name": str(message.author),
                            "icon_url": ICON_URL
                        },
                        "fields": [
                            {
                                "name": "Gönderilen Mesaj",
                                "value": message.content,
                                "inline": False
                            }
                        ],
                        "footer": {
                            "text": "DM ile gönderilen mesaj"
                        }
                    }
                ]
            }
            
            # Webhook isteği gönder
            requests.post(WEBHOOK_URL, json=embed)

async def setup(bot):
    await bot.add_cog(DMListener(bot))
