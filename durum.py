import discord
from discord.ext import commands

class BotDurumu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='durum', help='Botun çevrimiçi durumunu değiştirir.')
    @commands.has_permissions(administrator=True)  # Sadece yetkili kullanıcılar kullanabilir
    async def durum(self, ctx, *, durum: str):
        # Durumları tanımlayın
        durumlar = {
            'çevrimiçi': discord.Status.online,
            'rahatsız_etmeyin': discord.Status.dnd,
            'boşta': discord.Status.idle,
            'görünmez': discord.Status.invisible
        }

        # Geçerli bir durum olup olmadığını kontrol edin
        if durum not in durumlar:
            await ctx.send("Geçersiz durum. Geçerli durumlar: çevrimiçi, rahatsız_etmeyin, boşta, görünmez.")
            return

        # Botun durumunu ayarla
        await self.bot.change_presence(status=durumlar[durum])
        await ctx.send(f"Botun durumu '{durum}' olarak değiştirildi.")

async def setup(bot):
    await bot.add_cog(BotDurumu(bot))
