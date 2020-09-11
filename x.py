import discord
from discord.ext import commands


class X(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def x(self, ctx):
        jason = self.bot.get_user(532264643771629580)
        await ctx.send(jason.mention)
