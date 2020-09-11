from discord.ext import commands


class Sleep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sleepers = set()

    @commands.group()
    async def sleep(self,ctx):
        if ctx.invoked_subcommand is None:
            ctx.send('zzzzzzz')

    @sleep.command()
    async def add(self, ctx):
        for mention in ctx.message.mentions:
            self.sleepers.add(mention)
            await ctx.send(f'Shhhhhhh {mention.mention}')

    @sleep.command()
    async def remove(self, ctx):
        message = ctx.messsage
        for mention in message.mentions:
            if message.author != mention:
                self.sleepers.remove(mention)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author in self.sleepers:
            await message.author.create_dm()
            await message.author.dm_channel.send('GO TO SLEEP!!')
