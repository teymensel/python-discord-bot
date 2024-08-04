import sys
import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import datetime
import requests  # HTTP istekleri için

# .env dosyasını yükle
load_dotenv()

# Çevre değişkenlerini al
TOKEN = os.getenv('BOT_TOKEN')
PREFIX = os.getenv('PREFIX', '!')
STATUS = os.getenv('STATUS', 'playing')
STATUS_MESSAGE = os.getenv('STATUS_MESSAGE', 'with your commands!')
API_URL = 'https://teymensel.com/yapayzeka/api.php'
API_KEY = 'YOUR_API_KEY'  # API anahtarınızı buraya ekleyin

# İntentleri tanımlama
intents = discord.Intents.default()
intents.message_content = True  # Mesaj içeriğine erişim izni

# Bot'un prefixi ve tanımı
bot = commands.Bot(command_prefix=PREFIX, description="Vexon Bot", intents=intents)

# Botun başlangıç zamanını kaydetme
bot.launch_time = datetime.datetime.now(datetime.timezone.utc)

def restart_bot():
    """Botu yeniden başlatır."""
    os.execv(sys.executable, [sys.executable] + sys.argv)

@bot.command(name='restart')
@commands.has_permissions(administrator=True)  # Sadece yetkili kullanıcılar kullanabilir
async def restart(ctx):
    await ctx.send("Bot yeniden başlatılıyor...")
    restart_bot()

# Soruyu API'ye gönder ve cevabı al
async def get_answer_from_ai(question):
    headers = {
        'Content-Type': 'application/json',
    }
    payload = {
        'question': question
    }
    response = requests.post(f'{API_URL}?key={API_KEY}', json=payload, headers=headers)
    data = response.json()
    return data.get('response', 'Bilinmiyor')

# Komut dosyalarını yükleme
async def load_commands():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f'{filename} yüklendi.')
            except Exception as e:
                print(f'{filename} yüklenemedi. Hata: {e}')

# Slash komutlarını yükleme
async def load_slash_commands(path='./slash_commands'):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path):
            # Alt klasörler varsa, onları da tarayın
            await load_slash_commands(file_path)
        elif filename.endswith('.py'):
            try:
                module_path = f'slash_commands.{os.path.relpath(file_path, start="./slash_commands").replace(os.sep, ".")[:-3]}'
                await bot.load_extension(module_path)
                print(f'Slash komutu {filename} yüklendi.')
            except Exception as e:
                print(f'Slash komutu {filename} yüklenemedi. Hata: {e}')

# Bot hazır olduğunda çağrılır
@bot.event
async def on_ready():
    print(f'{bot.user.name} olarak giriş yapıldı.')
    print('Yüklenmiş komutlar:')
    for command in bot.commands:
        print(command.name)

    # Durum mesajını ayarla
    status_type = getattr(discord.ActivityType, STATUS, discord.ActivityType.playing)
    activity = discord.Activity(type=status_type, name=STATUS_MESSAGE)
    await bot.change_presence(activity=activity)

    # Komutları yükle
    await load_commands()
    # Slash komutlarını yükle
    await load_slash_commands()
    # Slash komutlarını Discord'a kaydet
    await bot.tree.sync()

    # Ping değerini yazdır
    latency = bot.latency * 1000  # ms cinsinden
    print(f'Ping: {latency:.2f} ms')

    # Botun açık kalma süresini yazdır
    uptime = datetime.datetime.now(datetime.timezone.utc) - bot.launch_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f'Açık Kalma Süresi: {days} gün, {hours} saat, {minutes} dakika, {seconds} saniye')

# Soruyu API'ye gönder ve cevabı döndür
@bot.command(name='soru')
async def soru(ctx, *, question):
    answer = await get_answer_from_ai(question)
    await ctx.send(f'{answer}')

# Bot token'ını güvenli bir şekilde saklayın
if TOKEN:
    bot.run(TOKEN)
else:
    print("Lütfen bot token'ınızı .env dosyasına ekleyin.")
