import requests
from discord import Color
from discord.ext import commands
import discord
import asyncio


class Mine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.short_delay = 300
        self.servers = {}
        self.add_server('cezarlinux.net', 762491809157873694, contact=468602065757798420)

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
                # if True:
                await self.send_status_message(addr)

    def get_server_status(self, address):
        API_URL = 'https://api.mcsrvstat.us/2/'
        resp = requests.get(API_URL + address)
        if resp.status_code != 200:
            raise IOError('Could not access api')
        status = resp.json()
        del status['debug']
        return status

    async def send_status_message(self, addr):
        channel: discord.TextChannel = self.bot.get_channel(self.servers[addr]['channel_id'])
        await channel.send(embed=self.create_status_message(addr))
        if not self.servers[addr]['status']['online']:
            contact = self.bot.get_user(self.servers[addr]['emerge_contact'])
            await  channel.send(contact.mention)

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

    def add_server(self, addr, id, contact=None):
        self.servers[addr] = {}
        self.servers[addr]['status'] = {}
        self.servers[addr]['channel_id'] = id
        self.servers[addr]['emerge_contact'] = contact

    def get_players(self, players):
        out = f'Online: {players["online"]}\n'
        for player in players['list']:
            out += f'  {player}\n'
        return out


if __name__ == '__main__':
    Mine(None)
