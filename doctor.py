from discord.ext import commands


class Doctor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sleepers = set()

    @commands.group()
    async def doctor(self,ctx):
        if ctx.invoked_subcommand is None:
            ctx.send('zzzzzzz')

    @doctor.command()
    async def add(self, ctx):
        for mention in ctx.message.mentions:
            self.sleepers.add(mention)
            await ctx.send(f'You were warned {mention.mention}')

    @doctor.command()
    async def remove(self, ctx):
        message = ctx.message
        for mention in message.mentions:
            if message.author != mention:
                self.sleepers.remove(mention)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author in self.sleepers:
            await message.author.create_dm()
            await message.author.dm_channel.send('GO SEE A DOCTOR!!')
