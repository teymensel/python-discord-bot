import discord
from discord.ext import commands
import os

class AutoBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ban_list_path = './auto_ban_list.txt'  # Yasaklama listesinin dosya yolu

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """Yeni bir üye sunucuya katıldığında otomatik yasaklama kontrolü yapar."""
        if not member.bot:
            # Yasaklama listesine bak
            if os.path.exists(self.ban_list_path):
                with open(self.ban_list_path, 'r') as file:
                    lines = file.readlines()
                
                for line in lines:
                    user_id, sebep = line.strip().split(' - Sebep: ')
                    if int(user_id) == member.id:
                        try:
                            await member.ban(reason=f"Otomatik yasaklama - Sebep: {sebep}")
                            print(f"{member} otomatik olarak yasaklandı. Sebep: {sebep}")
                        except discord.Forbidden:
                            print("Bu işlemi gerçekleştirmek için yeterli izniniz yok.")
                        except discord.HTTPException as e:
                            print(f"Bir hata oluştu: {str(e)}")
                        finally:
                            # Yasaklama işleminden sonra listeyi temizle
                            with open(self.ban_list_path, 'w') as file:
                                file.writelines([line for line in lines if line.strip().split(' - Sebep: ')[0] != str(member.id)])

async def setup(bot):
    await bot.add_cog(AutoBan(bot))
