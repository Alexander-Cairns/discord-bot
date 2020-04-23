import discord


class Sleep():
    def __init__(self):
        self.sleepers = set()

    def add_sleeper(self, message):
        for mention in message.mentions:
            self.sleepers.add(mention)

    def remove_sleeper(self, message):
        for mention in message.mentions:
            if message.author != mention:
                self.sleepers.remove(mention)

    async def go_to_sleep(self, message):
        if message.author in self.sleepers:
            print('yay')
            await message.author.create_dm()
            await message.author.dm_channel.send('GO TO SLEEP!!')
