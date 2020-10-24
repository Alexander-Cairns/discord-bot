import json

from discord.ext import commands


class MessagePlayback(commands.Cog):
    def __init__(self, bot):
        try:
            with open('config/message_playback.json', 'r') as config:
                self.messages = json.load(config)
        except:
            self.messages = {}

    @commands.group(aliases=['mp'])
    async def message_playback(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Use this command to play back messages!')

    @message_playback.command(aliases=['a'])
    async def add(self, ctx, *, arg=None):
        if arg is None:
            await  ctx.send('This is not good')
            return
        space = arg.index(' ')
        list_name = arg[:space]
        message = arg[space + 1:]
        self.add_message(list_name, message)
        await ctx.send(f'{ctx.author.mention} I added \n > {message}\n to the list **{list_name}**')
        self.save()

    @message_playback.command(aliases=['ls', 'l'])
    async def list(self, ctx, list_name=None):
        if list_name is None:
            if len(self.messages) == 0:
                await ctx.send('No lists exist')
                return
            names = '\n'.join(list(self.messages.keys()))
            await ctx.send(f'The following lists exist:\n{names}')
        else:
            if list_name not in self.messages:
                await ctx.send('List does not exist')
                return
            msgs = '\n'.join(self.messages[list_name])
            await ctx.send(f'The list **{list_name}** constains:\n{msgs}')

    @message_playback.command(aliases=['p'])
    async def playback(self, ctx, list_name=None):
        if list_name is None:
            await ctx.send('This is not good')
        if list_name not in self.messages:
            await ctx.send('List does not exist')
        else:
            for message in self.messages[list_name]:
                await ctx.send(message)

    @message_playback.command(aliases=['rm', 'r'])
    async def remove(self, ctx, list_name=None, index=-1):
        if list_name is None:
            await ctx.send('This is not good')
        if list_name not in self.messages:
            await ctx.send('List does not exist')
        if len(self.messages[list_name]) <= index:
            await ctx.send('Index not in list')
        if index == -1:
            del self.messages[list_name]
            await ctx.send(f'Removed the list **{list_name}**.')
            self.save()
        else:
            message = self.messages[list_name][index]
            del self.messages[list_name][index]
            if len(self.messages[list_name]) == 0:
                del self.messages[list_name]
            await ctx.send(f'Removed the message: \n> {message}\n from  the list **{list_name}**.')
            self.save()

    def add_message(self, list_name, message):
        if list_name not in self.messages:
            self.messages[list_name] = []
        self.messages[list_name].append(message)

    def save(self):
        with open('config/message_playback.json', 'w') as config:
            config.write(json.dumps(self.messages, indent=2))
