from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, CommandStart
from configtest import token
import asyncio, logging


bot = Bot(token=token)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart())
async def start(message: Message):
    path = 'sticker.webm'
    stiker = FSInputFile(path)
    await bot.send_sticker(message.chat.id, sticker=stiker)


# @dp.message(Command('GIF'))
# async def gif(message: Message):
#     path = 'Aq.gif'
#     gif = FSInputFile(path)
#     await bot.send_animation(message.chat.id, sticker=gif)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())