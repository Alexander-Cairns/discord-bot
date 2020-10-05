import os
import re

import discord
import requests as requests
from discord.ext import commands


class Tex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = {}

    @commands.command()
    async def texl(self, ctx, *, arg=None):
        resp = requests.get(f'https://latex.codecogs.com/png.latex?%5Chuge%20{arg}')
        await self.send_image(ctx, resp.content, ctx.message)

    @commands.command()
    async def tex(self, ctx, *, arg=None):
        resp = requests.get(f'https://latex.codecogs.com/png.latex?%5Cbg_black%20%5Chuge%20{arg}')
        await self.send_image(ctx, resp.content, ctx.message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.id in self.messages:
            await self.messages[before.id].delete()
            arg = re.sub('\$texl? ', '', after.content)
            if after.content.startswith('$texl'):
                resp = requests.get(f'https://latex.codecogs.com/png.latex?%5Chuge%20{arg}')
            else:
                resp = requests.get(f'https://latex.codecogs.com/png.latex?%5Cbg_black%20%5Chuge%20{arg}')
            await self.send_image(after.channel, resp.content, after)
            self.messages.pop(before.id)

    async def send_image(self, target, image_data, source):
        image_name = f'tex/{source.id}.png'
        with open(image_name, 'wb') as file:
            file.write(image_data)
        with open(image_name, 'rb') as file:
            sent = await target.send(file=discord.File(file, 'new_filename.png'))
            self.messages[source.id] = sent
            os.system(image_name)
