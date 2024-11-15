from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio, logging
from config import token
import random



bot = Bot(token=token)
dp = Dispatcher()

user_data = {}

logging.basicConfig(level=logging.INFO)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Здарова Скуф, ты не занят?")
    user_data[message.from_user.id] = random.randint(1, 3)
    await message.answer("Я загадал число от 1 до 3, если угадаешь, то так уж и быть, получишь от меня приз")
    


@dp.message(lambda msg: msg.text.isdigit())
async def guess_number(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        await message.reply("Начни игру сначало лузер, отправив команду /start.")
        return

    try:
        user_guess = int(message.text)
        if user_guess < 1 or user_guess > 3:
            await message.reply("Выбери число от 1 до 3.")
            return

        random_number = user_data[user_id]

        if user_guess == random_number:
            await message.answer_photo(photo="https://media.makeameme.org/created/you-win-nothing-b744e1771f.jpg")
            del user_data[user_id]
        else:
            await message.answer_photo(photo='https://media.makeameme.org/created/sorry-you-lose.jpg')
            await message.reply(
                f"Загаданное число было: {random_number}. "
                "Попробуй ещё раз, или засыканул? :) /start."
            )
            del user_data[user_id]
    except ValueError:
        await message.reply("И чо это такое? Введи как человек или кто ты там.")






async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())