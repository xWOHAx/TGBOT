from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import asyncio


bot = Bot(token='7794857321:AAEsuSqmLvERU-oCS_jFz42y8enxM3bqOoE')
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! нужна помошь? -> /help")

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Доступные комманды: /start, /help, /about, /location, /contact, /info")


@dp.message(Command("contact"))
async def contact(message: Message):
    await message.answer_contact(first_name="Woha", last_name="IDK", phone_number='+996550960608')

@dp.message(Command('location'))
async def location(message: Message):
    await message.answer_location(latitude=40.52157915467634, longitude=72.79998740372552)

@dp.message(Command('about'))
async def about(message: Message):
    await message.answer("Меня зовут Шоха, родился 2005 году 4 марта. Учусь на программиста Back-End разработчиком.")
    await message.answer("Если тебя интересует IT курсы, то можешь смело начать учиться в It-Park. Подробнее в /info")

@dp.message(Command("info"))
async def about(message: Message):
    await message.answer_photo(photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSF_nfZKz-Qg4e8EkCrzOPgmMkhX1jdNsLp-Q&s')
    await message.answer("IT-Park — это захватывающее путешествие в мир технологий! Здесь вы освоите программирование, дизайн, разработку. Погрузитесь в реальные проекты и найдете свой путь в IT. Учитесь, создавайте и воплощайте мечты в жизнь вместе с нами!")
    await message.answer('А также есть соц. сети IT-Park. Все ссылки в /socialmedia')
    await message.answer("Какое направление IT тебя интересует?")
    await message.answer("Back-End? Front-End или UI UX?")

@dp.message(Command('socialmedia'))
async def socialmedia(message: Message):
    await message.answer("Ссылка на Инстаграм - https://www.instagram.com/itpark_osh/")
    await message.answer('Ссылка на Facebook - https://www.facebook.com/237613209431104')


@dp.message(F.text =='UI UX')
async def hello(message: Message):
    await message.answer('UI/UX — это дизайн и пользовательский опыт. UI (User Interface) создает красивый и удобный интерфейс, а UX (User Experience) заботится о том, чтобы взаимодействие с продуктом было комфортным и интуитивным.')
    
@dp.message(F.text == 'Back-End')
async def hello(message: Message):
    await message.answer('Back-End — это серверная часть разработки, которая отвечает за логику, базы данных и работу приложений «за кулисами». Здесь создаются мощные системы и API для взаимодействия с пользователями.') 
    
@dp.message(F.text == 'Front-End')
async def hello(message: Message):
    await message.answer('Front-End — это интерфейс и визуальная часть сайта или приложения. Разработчики Front-End превращают дизайнерские макеты в работающие страницы с помощью HTML, CSS и JavaScript.')  


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())