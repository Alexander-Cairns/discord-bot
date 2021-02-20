from discord.ext import commands
import discord
from PIL import Image
import io


def is_cropped(image: Image) -> bool:
    image = image.convert('RGB')
    px = image.load()
    for y in range(10, 30):
        for x in range(image.width // 4):
            r, g, b = px[x, y]
            if r + g + b >= 10:
                return False
    for y in range(image.height - 30, image.height - 10):
        for x in range(image.width // 4):
            r, g, b = px[x, y]
            if r + g + b >= 10:
                return False
    return True


class Cropped(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        for att in message.attachments:
            try:
                image_bytes = await att.read()
                if is_cropped(Image.open(io.BytesIO(image_bytes))):
                    resp = f'Please crop your images '
                    await message.reply(resp)
                    await message.delete()
            except:
                pass


if __name__ == '__main__':
    print(is_cropped(Image.open('image1.png')))
