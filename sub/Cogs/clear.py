import discord
from discord.ext import commands
import asyncio
import sqlite3

class Clear(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name = "주간숙제초기화")
    async def 숙제전체초기화(self, ctx):
        discord_id = str(ctx.author.id)
        conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level = None)
        c = conn.cursor ()

        c.execute("UPDATE characters SET boss1check = ?, boss2check = ?, boss3check = ? WHERE discord_id = ?", (0, 0, 0, discord_id))
        conn.commit()
        bot_message = await ctx.reply(f"{ctx.author.name}의 주간 숙제가 미완료로 변경되었습니다.")
        await asyncio.sleep(5)  # 5초 대기
        await ctx.message.delete()
        await bot_message.delete()  




async def setup(app):
    await app.add_cog(Clear(app))