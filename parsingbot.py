import sqlite3
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart, Command
import logging
import asyncio
from confog import token


logging.basicConfig(level=logging.INFO)


bot = Bot(token=token)
dp = Dispatcher()

parsing_active = False


conn = sqlite3.connect("news.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    news TEXT NOT NULL
)
""")
conn.commit()


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/news")],
        [KeyboardButton(text="/stop")]
    ],
    resize_keyboard=True
)


def parse_news():
    global parsing_active
    news_list = []
    count_news = 0

    for page in range(1, 3):
        if not parsing_active:
            break

        url = f'https://24.kg/page_{page}'
        response = requests.get(url=url)
        soup = BeautifulSoup(response.text, 'lxml')
        all_news = soup.find_all("div", class_="title")
        
        for news in all_news:
            if not parsing_active:
                break

            count_news += 1
            news_list.append(f"{count_news}. {news.text.strip()}")

    return news_list



@dp.message(CommandStart())
async def start_command(message: Message):
    await message.reply(
        "Привет! Я бот для парсинга новостей с 24.kg. Используй кнопки для работы.",
        reply_markup=keyboard
    )



@dp.message(Command("news"))
async def get_news(message: Message):
    global parsing_active
    parsing_active = True

    news = parse_news()
    if not news:
        await message.reply("Новости не найдены или парсинг был остановлен.")
        return

    for n in news:
        cursor.execute("INSERT INTO news (news) VALUES (?)", (n,))
    conn.commit()

    await message.reply("Новости успешно сохранены! Вот последние заголовки:")
    for n in news:
        await message.reply(n)



@dp.message(Command("stop"))
async def stop_command(message: Message):
    global parsing_active
    parsing_active = False 
    await message.reply("Парсинг остановлен. Для повтора вызовите /news.")



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())