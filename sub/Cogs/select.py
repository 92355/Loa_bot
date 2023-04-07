import discord
from discord.ext import commands

class SelectFunction1(discord.ui.Select):
    def __init__(self1):
        options = []
        options.append(discord.SelectOption(label='빙결오른',description='1530', value='빙결오른'))
        options.append(discord.SelectOption(label='빙결베인',description='1521', value='빙결베인'))
        options.append(discord.SelectOption(label='슈크림자몽',description='1521', value='슈크림자몽'))
        options.append(discord.SelectOption(label='환류일까점화일까',description='1475', value='환류일까점화일까'))
        options.append(discord.SelectOption(label='절구내발밑고정',description='1460', value='절구내발밑고정'))
        super().__init__(placeholder='캐릭터 선택', min_values=1, max_values=1, options=options)
        
    async def callback(self1, interaction: discord.Interaction):
        
        await interaction.channel.send(interaction.data["values"][0]+"을 선택하셨습니다.")
        await interaction.message.delete()


class SelectView1(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectFunction1())


class SelectFunction2(discord.ui.Select):
    def __init__(self2):
        options = []
        options.append(discord.SelectOption(label='발탄 하드',description='발하', value='발하'))
        options.append(discord.SelectOption(label='비아키스 하드',description='비하', value='비하'))
        options.append(discord.SelectOption(label='쿠크세이튼',description='쿠크', value='쿠크'))
        options.append(discord.SelectOption(label='아브렐슈드 노말',description='1~2관문', value='노브12'))
        options.append(discord.SelectOption(label='3~4관문',description='노말', value='노브34'))
        options.append(discord.SelectOption(label='5~6관문',description='노말', value='노브56'))
        options.append(discord.SelectOption(label='아브렐슈드 하드',description='1~2관문', value='하브12'))
        options.append(discord.SelectOption(label='3~4관문',description='하드', value='하브34'))
        options.append(discord.SelectOption(label='5~6관문',description='하드', value='하브56'))
        super().__init__(placeholder='군단장 선택', min_values=1, max_values=5, options=options)
        
    async def callback(self2, interaction: discord.Interaction):
        
        await interaction.channel.send(interaction.data["values"][0]+"을 선택하셨습니다.")
        await interaction.message.delete()


class SelectView2(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectFunction2())

class Select(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name='선택')
    async def select(self, ctx):
        await ctx.send("캐릭터선택", view=SelectView1())
        await ctx.send("군단장 선택", view=SelectView2())


async def setup(app):
    await app.add_cog(Select(app))