import os
import re

import discord
from discord.ext import commands
from pylatex import Document, Command, TextColor
from pylatex.utils import NoEscape


def img_from_latex(title, text, dark=True):
    background = '#36393E' if dark else 'white'
    textcolour = 'white' if dark else 'black'
    doc = Document(title)
    doc.documentclass = Command(
        'documentclass',
        options=['border=5pt'],
        arguments=['standalone'],
    )
    doc.append(TextColor(textcolour, NoEscape(text)))

    try:
        doc.generate_pdf(clean_tex=False)
    except:
        img_from_latex(title,'Please provide proper \LaTeX',dark)
        return


    os.system(
        f'convert -density 300 {title}.pdf -background "{background}" -flatten -quality 90 {title}.png')


class Tex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messages = {}

    @commands.command()
    async def texl(self, ctx, *, arg=None):
        title = f'tex/{ctx.message.id}'
        img_from_latex(title, arg, dark=False)
        with open(f'{title}.png', 'rb') as fp:
            sent = await ctx.send(file=discord.File(fp, 'new_filename.png'))
            self.messages[ctx.message.id] = sent
            os.system(f'rm {title}*')

    @commands.command()
    async def tex(self, ctx, *, arg=None):
        title = f'tex/{ctx.message.id}'
        img_from_latex(title, arg)
        with open(f'{title}.png', 'rb') as fp:
            sent = await ctx.send(file=discord.File(fp, 'new_filename.png'))
            self.messages[ctx.message.id] = sent
            os.system(f'rm {title}*')


    @commands.Cog.listener()
    async def on_message_edit(self,before,after):
        if before.id in self.messages:
            await self.messages[before.id].delete()
            arg = re.sub('\$texl? ','',after.content)
            title = f'tex/{after.id}'
            img_from_latex(title, arg)
            with open(f'{title}.png', 'rb') as fp:
                sent = await after.channel.send(file=discord.File(fp, 'new_filename.png'))
                self.messages[after.id] = sent
                os.system(f'rm {title}*')
            self.messages.pop(before.id)




if __name__ == '__main__':
    img_from_latex('tex/test', '$x^4$')
