import asyncio
import json

import discord
from discord import Color
from discord.ext import commands
from mcstatus import MinecraftServer


class Mine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.short_delay = 30
        self.config_file = 'minecraft_servers.json'
        try:
            with open(f'config/{self.config_file}', 'r') as config:
                self.servers = json.load(config)
        except:
            self.servers = {}

    @commands.group()
    async def mc(self, ctx):
        if ctx.invoked_subcommand is None:
            ctx.send('This is no good')

    @mc.command(aliases=['a'])
    async def add(self, ctx, server=None):
        if server is None:
            await ctx.send('This is no good')
            return

        msg = ctx.message
        contact = msg.mentions[0].id if len(msg.mentions) > 0 else None
        self.add_server(server, ctx.channel.id, contact=contact)
        await ctx.send(f'Now monitoring {server}')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.watch_for_change()

    async def watch_for_change(self):
        while True:
            await self.update_servers()
            await asyncio.sleep(self.short_delay)

    async def update_servers(self):
        for addr in self.servers:
            old_status = self.servers[addr]['status']
            new_status = self.get_server_status(addr)
            self.servers[addr]['status'] = new_status
            if old_status != new_status:
                await self.send_status_message(addr)

    def get_server_status(self, address):
        server = MinecraftServer.lookup(address)
        try:
            status = server.status()
            status_dict = {'online': True,
                           'motd': {'clean': [m['text'] for m in status.description['extra']]},
                           'players': {
                               'online': status.players.online,
                               'max': status.players.max,
                               'list': [p.name for p in status.players.sample] if status.players.online > 0 else []
                           },
                           'hostname': server.host,
                           'port': server.port,
                           'software': status.version.name.split(' ')[0],
                           'version': ' '.join(status.version.name.split(' ')[1:]),
                           'protocol': status.version.protocol
                           }
            return status_dict
        except:
            return {'online': False, }

    async def send_status_message(self, addr):
        channel: discord.TextChannel = self.bot.get_channel(self.servers[addr]['channel_id'])
        await channel.send(embed=self.create_status_message(addr))
        if not self.servers[addr]['status']['online']:
            contact = self.bot.get_user(self.servers[addr]['emerge_contact'])
            if contact is not None:
                await channel.send(contact.mention)

    def create_status_message(self, addr):
        status = self.servers[addr]['status']
        print(status)
        emb = discord.Embed()
        emb.title = addr

        if not status['online']:
            emb.color = Color.red()
            emb.add_field(name='Status', value='offline')
            return emb

        emb.color = Color.green()
        emb.add_field(name='Status', value='online')
        emb.add_field(name='MOTD', value=status['motd']['clean'][0])
        emb.add_field(name='Players', value=self.get_players(status['players']), inline=True)

        emb.add_field(name='Version', value=f'{status["version"]}({status["software"]})')

        return emb

    def add_server(self, addr, channel_id, contact=None):
        self.servers[addr] = {}
        self.servers[addr]['status'] = {}
        self.servers[addr]['channel_id'] = channel_id
        self.servers[addr]['emerge_contact'] = contact
        self.save()

    def get_players(self, players):
        out = f'Online: {players["online"]}\n'
        if players['online'] > 0:
            for player in players['list']:
                out += f'  {player}\n'
        return out

    def save(self):
        with open(f'config/{self.config_file}', 'w') as config:
            config.write(json.dumps(self.servers, indent=2))


if __name__ == '__main__':
    pass
