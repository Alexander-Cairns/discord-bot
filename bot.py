from discord.ext.commands import Bot
import os

from covid import Covid
from dice import Dice
from help import Help
from hello import Hello
from landmine import Landmine
from sleep import Sleep
from x import X

bot = Bot(command_prefix='$')


@bot.listen()
async def on_ready():
    for guild in bot.guilds:
        print(f'Guild: {guild.name}, {guild.id}')

if __name__ == '__main__':
    bot.remove_command('help')
    bot.add_cog(Help(bot))
    bot.add_cog(Hello(bot))
    bot.add_cog(Covid(bot))
    bot.add_cog(X(bot))
    bot.add_cog(Dice(bot))
    bot.add_cog(Landmine(bot))
    bot.add_cog(Sleep(bot))

    TOKEN = os.environ['DISCORD_BOT_TOKEN']
    # sleepCommand = sleep.Sleep()
    bot.run(TOKEN)
