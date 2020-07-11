from random import randint
import discord
import requests
from lxml import html
import json
import re
import datetime
import os

import landmine
import dice
import sleep

client = discord.Client()


def get_covid_stats(location="PEI"):
    if location == 'PEI':
        page = requests.get(
                'https://www.princeedwardisland.ca/en/topic/covid-19').content
        x_paths = {
            'cases': '/html/body/div[2]/main/section/div/section/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div[1]/table/tbody/tr[3]/td[1]/text()',
            'negative': '/html/body/div[2]/main/section/div/section/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div[1]/table/tbody/tr[3]/td[2]/text()',
            'pending': '/html/body/div[2]/main/section/div/section/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div[1]/table/tbody/tr[3]/td[3]/text()',
            'recovered': '/html/body/div[2]/main/section/div/section/div/div/div[2]/div[1]/div[1]/div/div/div/div/div/div/div[1]/table/tbody/tr[3]/td[4]/text()'
        }
    tree = html.fromstring(page)
    stats = {
        'cases': parse_x('cases', tree, x_paths),
        'negative': parse_x('negative', tree, x_paths),
        'pending': parse_x('pending', tree, x_paths),
        'recovered': parse_x('recovered', tree, x_paths),
    }
    print(json.dumps(stats, indent=2))
    return stats


def parse_x(key, tree, paths):
    return int(re.sub(',', '', tree.xpath(paths[key])[0]))


@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'Guild: {guild.name}, {guild.id}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # if message.author.id == 435476534619537448:
    # if message.author.id == 468602065757798420:
    # await  message.channel.send(f'@{message.author} GO TO BED')
    if message.content == '!hello':
        await message.channel.send('Hello, World!')
    if message.content == '!covid update':
        now = datetime.datetime.now()
        date = now.strftime('%a %b %d %Y')
        time = now.strftime('%I %p')
        resp = f'Covid-19 cases for PEI as of {date} at {time}\n ```json\n{json.dumps(get_covid_stats(), indent=2)}\n```'
        await message.channel.send(resp)
    if message.content == '!help':
        await message.channel.send('is easy!')
    if message.content.startswith('!roll'):
        resp = dice.discord_dice(message.content)
        await message.channel.send(resp)
    if randint(1, 100) == 1 \
            or message.guild.name == 'Marky Mark and the Funky Bunch':
        await message.channel.send(landmine.death(message.content))
    if message.content.lower().startswith('!x'):
        await message.channel.send('```json\n{\n  "X": "JASON!!!!!"\n}\n```')
    if message.content.lower().startswith('!go to sleep'):
        sleepCommand.add_sleeper(message)
    if message.content.lower().startswith('!stop sleep'):
        sleepCommand.remove_sleeper(message)
    await sleepCommand.go_to_sleep(message)


if __name__ == '__main__':
    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    sleepCommand = sleep.Sleep()
    client.run(TOKEN)
