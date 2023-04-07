import os
import asyncio
import discord
from discord.ext import commands
import sqlite3
import requests
from bs4 import BeautifulSoup
class week_corps_list(commands.Cog):
    def __init__(self, app):
        self.app = app
        
    @commands.command(name='숙제표')
    async def week_corps_list(self, ctx):
            discord_id = str(ctx.author.id)

            conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level = None)
            c = conn.cursor ()
            c.execute("SELECT character_name, item_level, boss1, boss1check, boss2, boss2check, boss3, boss3check FROM characters WHERE discord_id = ?", (discord_id,))
            characters = c.fetchall()

            # c_conn = sqlite3.connect(f"DB/Corps_reward"'.db', isolation_level = None)
            # c = c_conn.cursor ()

            # c.execute("SELECT * FROM reward WHERE Corps = ? and grade = ?", (corps_name, lod))
            # reward_info = c.fetchone()


            if len(characters) > 0:
                await ctx.send(f"{ctx.author.mention} 님의 캐릭터 정보:\n")
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
                    embed.add_field(name=f" \n", value="", inline=True)
                bot_message = await ctx.send(embed=embed)

            
            else:
                bot_message = await ctx.reply(f"{ctx.author.mention} 님은 아직 캐릭터 정보를 등록하지 않았습니다.")
                await asyncio.sleep(5)  # 3초 대기
                await ctx.message.delete()
                await bot_message.delete() 

    

async def setup(app):
    await app.add_cog(week_corps_list(app))

    