import sqlite3
from discord.ext import commands
import asyncio

class db_register(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command( name = '가입')
    async def register(self, ctx):
        discord_id = str(ctx.author.id)

        conn = sqlite3.connect(f"{discord_id}"'.db', isolation_level=None)

        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS characters
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             discord_id TEXT,
             character_name TEXT,
             item_level INTEGER,
             boss1 TEXT,
             boss1grade TEXT,
             boss1gate INTEGER,
             boss1check INTEGER,
             boss2 TEXT,
             boss2grade TEXT,
             boss2gate INTEGER,
             boss2check INTEGER,
             boss3 TEXT,
             boss3grade TEXT,
             boss3gate INTEGER,
             boss3check INTEGER)''')
        await ctx.reply(f"{ctx.author.mention}님! 환영합니다!! DB등록이 완료되었어요!.\n '!캐릭터등록'을 입력해보세요!")


def setup(bot):
    bot.add_cog(db_register(bot))


async def setup(app):
    await app.add_cog(db_register(app))