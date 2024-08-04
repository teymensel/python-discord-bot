import mysql.connector  # MySQL bağlantısı için
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests

# .env dosyasını yükle
load_dotenv()

# API URL ve anahtar
API_URL = 'https://teymensel.com/yapayzeka/api.php'
API_KEY = 'YOUR_API_KEY'  # API anahtarınızı buraya ekleyin

# Veritabanı bağlantısı bilgileri
DB_HOST = '31.186.11.112'  # Veritabanı sunucusu
DB_USER = 'kon362npatcomtr_vexonadmin'  # Veritabanı kullanıcı adı
DB_PASS = 'S2mle100lesh911'  # Veritabanı şifresi
DB_NAME = 'kon362npatcomtr_vexonbot'  # Veritabanı adı

# Yapay Zeka Komutları
class YapayZeka(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_server_ai_status(self, server_id):
        """Sunucunun yapay zeka ayarını veritabanından alır."""
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT yapaysohbet FROM public WHERE serverid = %s", (server_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 'hayır'

    async def get_answer_from_ai(self, question):
        """API'ye soruyu gönderir ve cevabı alır."""
        headers = {'Content-Type': 'application/json'}
        payload = {'question': question}
        response = requests.post(f'{API_URL}?key={API_KEY}', json=payload, headers=headers)
        data = response.json()
        return data.get('response', 'Bilinmiyor')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        
        server_id = str(message.guild.id)  # Sunucu ID'si
        ai_status = await self.get_server_ai_status(server_id)

        # Komutları kontrol et
        if ai_status == 'evet' and (
            message.content.startswith('vexon') or
            message.content.startswith('v! soru') or
            message.content.startswith('<@1226859966862983290>')
        ):
            # Soru içeren mesajı ayıkla
            question = message.content.split(maxsplit=1)[1] if len(message.content.split()) > 1 else ''
            if question:
                answer = await self.get_answer_from_ai(question)
                await message.channel.send(f'{answer}')

async def setup(bot):
    await bot.add_cog(YapayZeka(bot))
