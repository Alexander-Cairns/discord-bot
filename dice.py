from random import randint
from discord.ext import commands
from lark import Lark

class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self,ctx, *,arg):
        rolls = parse(arg)
        resp = f'{ctx.author.mention}\n'
        for num, die, adv, add in rolls:

            total, sub_rolls = get_rolls(num, die, adv, add)
            if num > 1:
                resp += f'{num}d{die}: {total}, {sub_rolls}\n'
            else:
                resp += f'{num}d{die}: {total}\n'
                if adv != 0:
                    resp += f' {sub_rolls[0]}\n'
        await  ctx.send(resp)

def parse(text):
    print(text)
    parser = Lark(r"""
    rolls: roll+ 
    roll: [num] "d" die mod*
    num: SIGNED_NUMBER
    die: SIGNED_NUMBER
    mod: adv | dis | math
    adv: /adv/ 
    dis: /dis/
    math: op SIGNED_NUMBER
    op: /\+/ | /-/
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
    """, start='rolls')
    tree = parser.parse(text)
    rolls = []
    for roll in tree.children:
        adv = 0
        add = 0
        num = 1
        die = 0
        for child in roll.children:
            if child.data == 'num':
                num = int(child.children[0])
            if child.data == 'die':
                die = int(child.children[0])
            if child.data == 'mod':
                for mod in child.children:
                    if mod.data == 'adv':
                        adv += 1
                    if mod.data == 'dis':
                        adv -= 1
                    if mod.data == 'math':
                        op = mod.children[0].children[0]
                        val = mod.children[1]
                        if op == '+':
                            add += int(val)
                        if op == '-':
                            add -= int(val)
        rolls.append((num, die, adv, add))
    return rolls


def get_rolls(num, sides, adv, add):
    total = 0
    rolls = []
    for i in range(num):
        roll1 = randint(1, sides)
        roll2 = randint(1, sides)
        if adv >= 1:
            total += max(roll1, roll2)
            rolls.append((roll1, roll2))
        elif adv <= -1:
            total += min(roll1, roll2)
            rolls.append((roll1, roll2))
        else:
            total += roll1
            rolls.append(roll1)

    if add > 0:
        total = f'{total + add} ({total} + {add})'
    if add < 0:
        total = f'{total + add} ({total} - {-add})'
    return total, rolls

