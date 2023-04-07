import sqlite3
import discord
from discord.ext import commands
import asyncio

class Rewards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect(f"DB/Corps_reward.db", isolation_level=None)
        self.c = self.conn.cursor()

    @commands.command( name = '보상')
    async def reward(self, ctx):
        corps_name = await ctx.send("보상을 확인할 레이드 이름을 입력하세요 : ")
        corps_name = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=10.0)

        corps_name = corps_name.content
        lod = await ctx.send("난이도를 입력하세요:")
        lod = await self.bot.wait_for('message', check=lambda msg: msg.author == ctx.author, timeout=10.0)
        lod = lod.content

        if lod.lower() in ['n', '노말', 'nomal', '1']:
            lod = 'Nomal'
        elif lod.lower() in ['h', 'hard', '하드', '2']:
            lod = 'Hard'
        else:
            await ctx.send("잘못된 입력입니다.")

        self.c.execute("SELECT * FROM reward WHERE Corps = ? and grade = ?", (corps_name, lod))
        gold_reward = self.c.fetchall()
        total_gold = 0
        more_gold = 0
        if len(gold_reward) == 0:
            await ctx.send("해당하는 정보가 존재하지 않습니다.")
        else:
            for row in gold_reward:
                embed = discord.Embed(title =row[0],color=0x000000)
                embed.add_field(name ="난이도", value= f"{row[1]}", inline=True)
                embed.add_field(name ="관문", value= f"{row[2]}", inline=True)
                embed.add_field(name ="골드", value= "", inline=True)
                embed.add_field(name =f"+ {row[3]}", value="", inline=False)
                embed.add_field(name =f"- {row[4]}", value="", inline=False)
                embed.add_field(name ="아이템", value= "", inline=False)
                embed.add_field(name =f"{row[5]}", value= f"{row[6]}", inline=False)
                embed.add_field(name =f"{row[7]}", value= f"{row[8]}", inline=False)
                total_gold += int(row[3])
                embed.add_field(name =f"{total_gold}", value= "", inline=False)
                more_gold += int(row[4])
                await ctx.send(embed=embed)
        await ctx.send(f"총 획득 골드💵 {total_gold}G")
        await ctx.send(f"총 더보기 골드 : {more_gold}G")



def setup(bot):
    bot.add_cog(Rewards(bot))


async def setup(app):
    await app.add_cog(Rewards(app))