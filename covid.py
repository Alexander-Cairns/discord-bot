import datetime
import json
import re

import requests
from discord.ext import commands
from lxml import html


class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def covid(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Covid command')

    @covid.command()
    async def update(self, ctx):
        now = datetime.datetime.now()
        date = now.strftime('%a %b %d %Y')
        time = now.strftime('%I %p')
        resp = f'Covid-19 cases for PEI as of {date} at {time}\n'
        resp += f'```json\n{json.dumps(Covid.get_stats(), indent=2)}```'
        await ctx.send(resp)

    def get_stats(location="PEI"):
        if location == 'PEI':
            page = requests.get(
                'https://www.princeedwardisland.ca/en/information/health-and-wellness/pei-covid-19-case-data').content
            x_paths = {
                'cases': '/html/body/div[2]/main/section/div/section/div/div/div[3]/div[1]/div[2]/div[1]/div/div/div/div/div/table/tbody/tr[2]/td[2]/text()',
                'negative': '/html/body/div[2]/main/section/div/section/div/div/div[3]/div[1]/div[2]/div[1]/div/div/div/div/div/table/tbody/tr[5]/td[2]/text()',
                'pending': '/html/body/div[2]/main/section/div/section/div/div/div[3]/div[1]/div[2]/div[1]/div/div/div/div/div/table/tbody/tr[6]/td[2]/text()',
                'recovered': '/html/body/div[2]/main/section/div/section/div/div/div[3]/div[1]/div[2]/div[1]/div/div/div/div/div/table/tbody/tr[3]/td[2]/text()',
            }
        tree = html.fromstring(page)
        stats = {
            'cases': Covid.parse_x('cases', tree, x_paths),
            'negative': Covid.parse_x('negative', tree, x_paths),
            'pending': Covid.parse_x('pending', tree, x_paths),
            'recovered': Covid.parse_x('recovered', tree, x_paths),
        }
        print(json.dumps(stats, indent=2))
        return stats

    def parse_x(key, tree, paths):
        return int(re.sub('[,*]', '', tree.xpath(paths[key])[0]))
