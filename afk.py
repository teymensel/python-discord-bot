import discord
from discord.ext import commands
import sqlite3  # MySQL yerine SQLite kullanabilirsiniz, veya uygun bir veritabanı bağlayıcı kullanabilirsiniz

# Veritabanı bağlantısı
def connect_to_database():
    try:
        conn = sqlite3.connect('your_database.db')  # Veritabanı bağlantısını buraya koyun
        return conn
    except sqlite3.Error as e:
        print(f"Error: '{e}'")
        return None

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="afk", help="Kullanıcının AFK durumunu ayarlar.")
    async def afk(self, ctx, *, reason: str = None):
        if not reason:
            embed = discord.Embed(
                title="AFK Sistemi Nedir?",
                description=(
                    "**•** Eğer AFK olursanız ve birisi sizi etiketlerse, neden ve ne kadar süredir AFK olduğunuza dair bilgiler verir.\n"
                    "**•** AFK olabilmek için: `!afk <Sebep>` yazarak AFK olabilirsiniz.\n"
                    "**•** AFK'dan ayrılmak için: AFK olduğunuz sunucuda herhangi bir kanalda mesaj yazarak ayrılabilirsiniz."
                ),
                color=discord.Color.default()
            )
            embed.set_image(url='https://cdn.discordapp.com/attachments/768969206838067210/787314157597884416/unknown.png')
            await ctx.send(embed=embed)
            return

        if len(reason) > 500:
            embed = discord.Embed(
                title="Destan mı Yazıyorsun?",
                description="Kısalt şu uyarı sebebini, beni delirtme!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        # Veritabanına AFK durumunu kaydetme
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute('INSERT OR REPLACE INTO afk (user_id, reason, timestamp) VALUES (?, ?, ?)',
                           (ctx.author.id, reason, int(ctx.message.created_at.timestamp())))
            conn.commit()
            conn.close()

        # Kullanıcının takma adını değiştirme
        new_nickname = f"[AFK] {ctx.author.display_name}"
        if len(new_nickname) > 32:
            new_nickname = new_nickname[:32]
            embed = discord.Embed(
                title="Bilgi",
                description="Kullanıcı adı 32 karakteri geçtiği için ufak bir kırpma uygulandı.",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(color=discord.Color.green())

        try:
            await ctx.author.edit(nick=new_nickname)
            embed.title = f"{ctx.author.name}, artık AFK!"
            embed.add_field(name="Sebep", value=reason)
        except discord.Forbidden:
            embed.add_field(name="Bilgi", value="Kullanıcı adını düzenleme yetkim olmadığı için düzenleyemedim.")

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM afk WHERE user_id = ?', (message.author.id,))
            result = cursor.fetchone()
            if result:
                # AFK durumunu veritabanından sil
                cursor.execute('DELETE FROM afk WHERE user_id = ?', (message.author.id,))
                conn.commit()

                # Takma adını eski haline çevir
                old_nickname = message.author.display_name.replace("[AFK] ", "")
                try:
                    await message.author.edit(nick=old_nickname)
                    await message.channel.send(f"Artık AFK değilsiniz {message.author.mention}.")
                except discord.Forbidden:
                    await message.channel.send(f"Takma adınızı güncelleyemedim {message.author.mention}.")
            conn.close()

async def setup(bot):
    await bot.add_cog(AFK(bot))
