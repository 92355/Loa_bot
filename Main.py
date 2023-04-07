import os
import asyncio
import discord
from discord.ext import commands
import sqlite3
import requests
from bs4 import BeautifulSoup
# conn = sqlite3.connect("database.db", isolation_level = None)
# c = conn.cursor ()


#############################아이템 레벨 구간탐색#############
def section(x):
    result = []
    levels = [
        (1370, 1474, "노루"),
        (1415, 1445, "발노"),
        (1445, 1490, "발하"),
        (1430, 1460, "비노"),
        (1460, 1580, "비하"),
        (1475, 1656, "쿠크"),
        (1490, 1500, "노브 1 ~ 2"),
        (1500, 1520, "노브 1 ~ 4"),
        (1520, 1540, "노브 1 ~ 6"),
        (1540, 1550, "하브 1 ~ 2 노브 3 ~ 6"),
        (1550, 1560, "하브 1 ~ 4 노브 5 ~ 6"),
        (1560, 1656, "하브 1 ~ 6"),
        (1580, 1600, "노칸 1 ~ 3"),
        (1600, 1656, "하칸 1 ~ 3"),
    ]
    for level in levels:
        if level[0] <= x < level[1]:
            result.append(level[2])
    if result:
        return ", ".join(result)
    else:
        return "해당하는 구간이 없습니다."

############################## 템렙 검색 ################
def get_character_info(name):
    url = f"https://lostark.game.onstove.com/Profile/Character/{name}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    item_level_1 = soup.find('div', {'class': 'level-info2'}).find_all('span')[1].text
    item_level = int(float(item_level_1.replace(',', '').replace('Lv.', '')))
    return item_level





intents = discord.Intents.all()

bot = commands.Bot(command_prefix = '/', intents=intents)

@bot.event
async def on_ready():
    print("starting................................................")

@bot.command()
async def 도움말(ctx):
    helpembed=discord.Embed(title="도움말 ")
    helpembed.add_field(name="!정보 XXX", value="아이템 레벨, 숙제 보기", inline=False)
    helpembed.add_field(name="!디비등록", value="최초 사용시 데이터 베이스 만들기", inline=False)
    helpembed.add_field(name="!캐릭터등록 XXX", value="(최초1 회 등록) XXX 캐릭터를 데이터 베이스에 등록", inline=False)
    # helpembed.add_field(name="!캐릭터업데이트", value="숙제 구간이 변경되면 입력하세요", inline=False)
    helpembed.add_field(name="!숙제표", value="등록된 캐릭터의 숙제내역 확인", inline=False)
    helpembed.add_field(name="!모바일숙제", value="모바일 버전 숙제표", inline=False)
    helpembed.add_field(name="!완료 N XXX", value="XXX캐릭터의 N번째 숙제 완료 체크", inline=False)
    helpembed.add_field(name="!미완료 N XXX", value="XXX 캐릭터의 N번째 숙제 완료내역 초기화", inline=False)
    helpembed.add_field(name="!캐릭터삭제 XXX", value="데이터베이스에서 캐릭터 정보 삭제", inline=False)
    helpembed.add_field(name="!주간숙제초기화", value="주간숙제 전체 미완료 처리", inline=False)
    helpembed.add_field(name="!공략", value="군단장 컨닝페이퍼", inline=False)
    helpembed.add_field(name="!보상", value="관문 보상 확인 골드, 아이템 ", inline=False)
    await ctx.send(embed=helpembed)
########################################
########################################
########################################
########################################    

#템레벨검색, 군단장 정보
@bot.command(name='정보')
async def character_info(ctx, name):
    item_level = get_character_info(name)
    corps = section(item_level)

    embed=discord.Embed(title="캐릭터 정보 ")
    embed.add_field(name=f"{name}", value='⚔️'f"{item_level}"+"\n"+f"{corps}", inline=False)
    bot_message = await ctx.send(embed=embed)
    await asyncio.sleep(1800)  # 5초 대기
    await ctx.message.delete()
    await bot_message.delete() 
########################################
########################################
########################################
########################################    

#디비만들기
@bot.command(name = "디비등록")
async def DB_add(ctx):
    discord_id = str(ctx.author.id)

    conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level=None)

    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS characters
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                discord_id TEXT,
                character_name TEXT,
                item_level INTEGER,
                boss1 TEXT,
                boss1check INTEGER,
                boss2 TEXT,
                boss2check INTEGER,
                boss3 TEXT,
                boss3check INTEGER)''')  
    await ctx.reply(f"{ctx.author.mention}님! 환영합니다!! DB등록이 완료되었어요!.\n '!캐릭터등록'을 입력해보세요!")
########################################
########################################
########################################
########################################
#캐릭터등록
@bot.command()
async def 캐릭터등록(ctx, name: str):

    discord_id = str(ctx.author.id)
    conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level = None)
    c = conn.cursor ()
    
    item_level = get_character_info(name)
    corps = section(item_level).split(",")
    boss1check = 0
    boss2check = 0
    boss3check = 0
    c.execute("INSERT INTO characters (discord_id, character_name, item_level, boss1, boss1check, boss2, boss2check, boss3, boss3check) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (discord_id, name, item_level, corps[0], boss1check, corps[1], boss2check, corps[2], boss3check))
    conn.commit()

    bot_message = await ctx.reply(f"{ctx.author.mention} 님의 캐릭터 {name}의 정보가 저장되었습니다.")
    await asyncio.sleep(5)  # 5초 대기
    await ctx.message.delete()
    await bot_message.delete()  

# #캐릭터업데이트
# @bot.command()
# async def 캐릭터업데이트(ctx):
#     discord_id = str(ctx.author.id)
#     conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level = None)
#     c = conn.cursor ()

#     item_level = get_character_info(name)
#     corps = section(item_level).split(",")


#숙제 출력

########################################
########################################
########################################
########################################
# @bot.command()
# async def 숙제표(ctx):
#     discord_id = str(ctx.author.id)

#     conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level = None)
#     c = conn.cursor ()
#     c.execute("SELECT character_name, item_level, boss1, boss1check, boss2, boss2check, boss3, boss3check FROM characters WHERE discord_id = ?", (discord_id,))
#     characters = c.fetchall()

#     if len(characters) > 0:
#         await ctx.send(f"{ctx.author.mention} 님의 캐릭터 정보:\n")
#         embed = discord.Embed(title="캐릭터 목록", color=0x00ff00)
#         for character in characters:
#             if character[3] == 0:
#                 boss1_emoji = "❌"
#             else:
#                 boss1_emoji = "👌"

#             if character[5] == 0:
#                 boss2_emoji = "❌"
#             else:
#                 boss2_emoji = "👌"

#             if character[7] == 0:
#                 boss3_emoji = "❌"
#             else:
#                 boss3_emoji = "👌"
#             embed.add_field(name=f"@{character[0]} ({character[1]})", value="", inline=False)
#             embed.add_field(name=f" {character[2]}", value=f"1 {boss1_emoji}", inline=True)
#             embed.add_field(name=f" {character[4]}", value=f"2 {boss2_emoji}", inline=True)
#             embed.add_field(name=f" {character[6]}", value=f"3 {boss3_emoji}", inline=True)
#             embed.add_field(name=f" \n", value="", inline=True)
#         bot_message = await ctx.send(embed=embed)

    
#     else:
#         bot_message = await ctx.reply(f"{ctx.author.mention} 님은 아직 캐릭터 정보를 등록하지 않았습니다.")
#         await asyncio.sleep(5)  # 3초 대기
#         await ctx.message.delete()
#         await bot_message.delete() 
########################################
########################################
########################################
########################################
########################################
########################################
@bot.command()
async def 모바일숙제표(ctx):
    discord_id = str(ctx.author.id)
    conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level = None)
    c = conn.cursor ()
    c.execute("SELECT character_name, item_level, boss1, boss1check, boss2, boss2check, boss3, boss3check FROM characters WHERE discord_id = ?", (discord_id,))
    characters = c.fetchall()
    bot_message_delete = []
    if len(characters) > 0:
        message = await ctx.send(f"{ctx.author.mention} 님의 캐릭터 정보:\n")
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
            msg = f"@{character[0]} ({character[1]}) \n {character[2]} {character[4]} {character[6]} \n 1 {boss1_emoji} 2 {boss2_emoji}  3 {boss3_emoji} \n----------------------"
            bot_message = await ctx.send(msg)
            bot_message_delete.append(bot_message)
            
        await asyncio.sleep(10)  # 10초 대기
        await ctx.message.delete()
        await message.delete()
        for bot_message in bot_message_delete:
            await bot_message.delete()
    
    else:
        bot_message = await ctx.reply(f"{ctx.author.mention} 님은 아직 캐릭터 정보를 등록하지 않았습니다.")
        await asyncio.sleep(5)  # 5초 대기
        await ctx.message.delete()
        await bot_message.delete()
########################################

#숙제 미완

@bot.command(name = "미완료")
async def complete_id(ctx, boss_num, msg):
    discord_id = str(ctx.author.id)
    conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level = None)
    c = conn.cursor ()

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
        if message.author == bot.user and message.embeds:
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

    bot_message = await ctx.reply(f"{msg}의 {boss_num}번 숙제가 미완료로 변경 되었습니다. \n (이 메세지는 3초후 삭제됩니다)")
    await asyncio.sleep(3)  # 3초 대기
    await ctx.message.delete()
    await bot_message.delete()  

########################################
########################################
########################################
########################################
@bot.command()
async def 캐릭터삭제(ctx, msg):
    discord_id = str(ctx.author.id)
    conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level = None)
    c = conn.cursor ()

    msg = str(msg)
    c.execute("DELETE From characters  WHERE character_name = ?", (msg,))
    conn.commit()
    bot_message = await ctx.reply(f"데이터베이스에서 {msg}가 삭제되었습니다.")
    await ctx.message.delete()
    await bot_message.delete()  
########################################
########################################
########################################
########################################
#디비 초기화
@bot.command(name = "1022")
async def refresh(ctx):
    discord_id = str(ctx.author.id)
    conn = sqlite3.connect(f"DB/{discord_id}"'.db', isolation_level = None)
    c = conn.cursor ()
    conn.execute("DELETE FROM characters ")
    conn.execute("select * from characters")
    await ctx.message.delete()
########################################
########################################
########################################
########################################
########################################
########################################
########################################
########################################
#Cogs Load
async def load_extensions():
    for filename in os.listdir("Cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"Cogs.{filename[:-3]}")


@bot.command(name="reload")
async def reload_extension(ctx, extension=None):
    if extension is not None:
        await unload_function(extension)
        try:
            await bot.load_extension(f"Cogs.{extension}")
        except commands.ExtensionNotFound:
            await ctx.send(f":x: '{extension}'을(를) 파일을 찾을 수 없습니다!")
        except (commands.NoEntryPointError, commands.ExtensionFailed):
            await ctx.send(f":x: '{extension}'을(를) 불러오는 도중 에러가 발생했습니다!")
        else:
            await ctx.send(f":white_check_mark: '{extension}'을(를) 다시 불러왔습니다!")
    else:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                await unload_function(filename[:-3])
                try:
                    await bot.load_extension(f"Cogs.{filename[:-3]}")
                except commands.ExtensionNotFound:
                    await ctx.send(f":x: '{filename[:-3]}'을(를) 파일을 찾을 수 없습니다!")
                except (commands.NoEntryPointError, commands.ExtensionFailed):
                    await ctx.send(f":x: '{filename[:-3]}'을(를) 불러오는 도중 에러가 발생했습니다!")
        await ctx.send(":white_check_mark: reload 작업을 완료하였습니다!")


@bot.command(name="unload")
async def unload_extension(ctx, extension=None):
    if extension is not None:
        await unload_function(extension)
        await ctx.send(f":white_check_mark: {extension}기능을 종료했습니다!")
    else:
        await unload_function(None)
        await ctx.send(":white_check_mark: 모든 확장기능을 종료했습니다!")


async def unload_function(extension=None):
    if extension is not None:
        try:
            await bot.unload_extension(f"Cogs.{extension}")
        except (commands.ExtensionNotLoaded, commands.ExtensionNotFound):
            pass
    else:
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.unload_extension(f"Cogs.{filename[:-3]}")
                except (commands.ExtensionNotLoaded, commands.ExtensionNotFound):
                    pass


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="몰?루", description="입력하신 명령어는 존재하지 않는 명령어입니다", color=0xFF0000)
        await ctx.reply(embed=embed)
        return
    else:
        embed = discord.Embed(title="오류!!", description="예상치 못한 오류가 발생했습니다.", color=0xFF0000)
        embed.add_field(name="상세", value=f"```{error}```")
        await ctx.reply(embed=embed)
        return


async def main():
    async with bot:
    
        await load_extensions()
        
        file = open("token/FB_token.txt")
        bot_token = file.readline()
        file.close()
        await bot.start(bot_token)


asyncio.run(main())