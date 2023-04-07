import discord
from discord.ext import commands
import sqlite3


class SelectF(discord.ui.Select):
    def __init__(self, ctx):
        self.ctx = ctx
        discord_id = str(ctx.author.id)
        conn = sqlite3.connect(f"DB/{discord_id}.db", isolation_level=None)
        c = conn.cursor()
        c.execute("SELECT character_name, item_level FROM characters WHERE discord_id = ?", (discord_id,))
        characters = c.fetchall()
        conn.commit()
        options = []
        for character in characters:
            label = character[0]
            value = character[0]
            description = f"아이템 레벨: {character[1]}"
            option = discord.SelectOption(label=label, description=description, value=value)
            options.append(option)
        super().__init__(placeholder="캐릭터 선택", min_values=1, max_values=1, options=options)

    async def callback(self1, interaction: discord.Interaction):

        await interaction.channel.send(interaction.data["values"][0] + "을 선택하셨습니다.")
        await interaction.message.delete()

class SelectView1(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.add_item(SelectF(ctx))

class SelectComplete(commands.Cog):
    def __init__(self, app):
        self.app = app

    @commands.command(name="캐릭터셀렉트")
    async def select1(self, ctx):
        discord_id = str(ctx.author.id)
        await ctx.send("캐릭터선택", view=SelectView1(ctx))

async def setup(app):
    await app.add_cog(SelectComplete(app))
