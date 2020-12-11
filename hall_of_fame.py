
import json

from discord.ext import commands

class HallOfFame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open('config/hall_of_fame.json', 'r') as config:
                self.config = json.load(config)
        except:
            print('Could not load "config/hall_of_fame.json"')
            self.config = {}

    @commands.group(aliases=['hof'])
    async def hall_of_fame(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Use this command to manage the hall of fame!')

    @hall_of_fame.command()
    async def set(self, ctx):
        gid = str(ctx.guild.id)
        hofChannel = ctx.message.channel_mentions[0]
        if gid not in self.config:
            self.config[gid] = {'id': None, 'messages': []}
        self.config[gid]['channel_id'] = hofChannel.id
        await ctx.send(f'Hall of fame set to #{hofChannel}')
        self.save()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction,user):
        message = reaction.message
        gid = str(message.guild.id)
        if gid not in self.config:
            print('none')
            return
        hofChannel = self.bot.get_channel(self.config[gid]['channel_id'])
        num_reacts = 0
        for r in message.reactions:
            num_reacts += r.count
        if num_reacts >= 6 and message.id not in self.config[gid]['messages']:
            print(message.attachments)
            resp = ''
            resp+= '>>> '
            resp+= message.content
            resp+= f'\n{message.author.mention}'
            for att in message.attachments:
                resp+= f'\n{att.url}'
            await hofChannel.send(resp)
            self.config[gid]['messages'].append(message.id)
            self.save()

    def save(self):
        with open('config/hall_of_fame.json', 'w') as config:
            config.write(json.dumps(self.config, indent=2))
