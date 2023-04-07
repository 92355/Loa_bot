import discord
from discord.ext import commands

class SelectFunction(discord.ui.Select):
    def __init__(self):
        options = []
        options.append(discord.SelectOption(label='발탄',description='발탄-Nomal & Hard', value='Valtan'))
        options.append(discord.SelectOption(label='비아키스',description='비아키스-Nomal & Hard', value='Viakiss'))
        options.append(discord.SelectOption(label='쿠크세이튼',description='쿠크세이튼', value='koo'))
        options.append(discord.SelectOption(label='아브렐슈드 노말 12관문',description='1~2', value='Nob-12'))
        options.append(discord.SelectOption(label='아브렐슈드 노말 34관문',description='3~4', value='Nob-34'))
        options.append(discord.SelectOption(label='아브렐슈드 노말 56관문',description='5~6', value='Nob-56'))
        options.append(discord.SelectOption(label='아브렐슈드 하드 12관문',description='1~2', value='Hab-12'))
        options.append(discord.SelectOption(label='아브렐슈드 하드 34관문',description='3~4', value='Hab-34'))
        options.append(discord.SelectOption(label='아브렐슈드 하드 5관문',description='5', value='Hab-5'))
        options.append(discord.SelectOption(label='아브렐슈드 하드 6관문',description='6', value='Hab-6'))
        options.append(discord.SelectOption(label='프리우나 & 라우리엘',description='카양겔', value='Kaynaggel'))
        options.append(discord.SelectOption(label='일리아칸 노말 1관문',description='1', value='nokan-1'))
        options.append(discord.SelectOption(label='일리아칸 노말 2관문',description='2', value='nokan-2'))
        options.append(discord.SelectOption(label='일리아칸 노말 3관문',description='3', value='nokan-3'))
        options.append(discord.SelectOption(label='일리아칸 하드 12관문',description='1~2', value='hakan-12'))
        options.append(discord.SelectOption(label='일리아칸 하드 3관문',description='3', value='hakan-3'))
        super().__init__(placeholder='군단장선택', min_values=1, max_values=4, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        
        for value in interaction.data["values"]:
            if value.startswith(f"{value}"):
                with open(f"cnpp/{value}.jpeg", "rb") as f:
                    file = discord.File(f)
                    await interaction.channel.send(file=file)
        
        await interaction.message.delete()
        
class SelectView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(SelectFunction())

class cnpp(commands.Cog):
    def __init__(self, app):
        self.app = app
        
    @commands.command(name='공략')
    async def select(self, ctx):
        await ctx.send("컨닝페이퍼", view=SelectView())
        await ctx.message.delete()

async def setup(app):
    await app.add_cog(cnpp(app))