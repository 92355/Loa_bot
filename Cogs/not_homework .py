import discord
from discord.ext import commands
import sqlite3
import asyncio

class not_Homework(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name="미미완료")
    async def complete_id(self, ctx, boss_num, msg):
        discord_id = str(ctx.author.id)
        conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level=None)
        c = conn.cursor()

        msg = str(msg)

        if boss_num == '1':
            boss_col = 'boss1check'
            boss_name = 'boss1'
        elif boss_num == '2':
            boss_col = 'boss2check'
            boss_name = 'boss2'
        elif boss_num == '3':
            boss_col = 'boss3check'
            boss_name = 'boss3'
        else:
            await ctx.reply('보스 번호가 올바르지 않습니다.')
            return

        c.execute(f"UPDATE characters SET {boss_col} = ? WHERE character_name = ?", (0, msg))
        conn.commit()

        c.execute("SELECT character_name, item_level, boss1, boss1check, boss2, boss2check, boss3, boss3check FROM characters WHERE discord_id = ?", (discord_id,))
        characters = c.fetchall()
        async for message in ctx.history(limit=10):
            if message.author == self.app.user and message.embeds:
                if len(characters) > 0:
                    embed = discord.Embed(title="캐릭터 목록", color=0x00ff00)
                    for character in characters:
                        if character[3] == 0:
                            boss1_emoji = "❌"
                        else:
                            boss1_emoji = "👌"

                        if character[5] == 0:
                            boss2_emoji = "❌"
                        else:
                            boss2_emoji = "👌"

                        if character[7] == 0:
                            boss3_emoji = "❌"
                        else:
                            boss3_emoji = "👌"
                        embed.add_field(name=f"@{character[0]} ({character[1]})", value="", inline=False)
                        embed.add_field(name=f" {character[2]}", value=f"1 {boss1_emoji}", inline=True)
                        embed.add_field(name=f" {character[4]}", value=f"2 {boss2_emoji}", inline=True)
                        embed.add_field(name=f" {character[6]}", value=f"3 {boss3_emoji}", inline=True)
                await message.edit(embed=embed)
                break

        bot_message = await ctx.reply(f"{msg}의 {boss_num}번 숙제가 완료되었습니다. \n (이 메세지는 3초후 삭제됩니다)")
        await asyncio.sleep(3)  # 3초 대기
        await ctx.message.delete()
        await bot_message.delete()

async def setup(app):
    await app.add_cog(not_Homework(app))
