import discord
from discord.ext import commands
import os  # ✅ เพิ่มตรงนี้เพื่อใช้ Environment Variable

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ ตั้งค่า ID ให้ตรงกับของคุณ
REACTION_MESSAGE_ID = 1379067822843494590  # แทนด้วย Message ID ที่ให้กดอิโมจิ
ROLE_ID = 1378975589133717524             # แทนด้วย Role ID ที่จะแจก
LOG_CHANNEL_ID = 1378978265485541376      # แทนด้วย Channel ID ที่จะส่งประวัติ

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} พร้อมทำงานแล้ว!")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != REACTION_MESSAGE_ID:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    member = guild.get_member(payload.user_id)
    if not member or member.bot:
        return

    role = guild.get_role(ROLE_ID)
    if not role:
        return

    try:
        await member.add_roles(role, reason="Reaction role assignment")
        print(f"🎉 มอบยศ {role.name} ให้กับ {member.name}")

        # ส่ง Embed บันทึกไปยังห้อง log
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            embed = discord.Embed(
                title="✅ การยืนยันตัวตนเสร็จสมบูรณ์",
                description=f"{member.mention} ได้รับยศเรียบร้อย",
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
            embed.add_field(name="👤 ผู้ใช้", value=member.name, inline=True)
            embed.add_field(name="🆔 ID", value=member.id, inline=True)
            embed.add_field(name="🏷️ ยศที่ได้รับ", value=role.mention, inline=False)
            await log_channel.send(embed=embed)

    except discord.Forbidden:
        print("❌ บอทไม่มีสิทธิ์ให้ยศ")
    except Exception as e:
        print(f"⚠️ เกิดข้อผิดพลาด: {e}")

# ✅ เปลี่ยนให้ใช้ Token จาก Environment Variable
bot.run(os.environ["DISCORD_TOKEN"])
