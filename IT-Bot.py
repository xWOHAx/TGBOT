from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart, Command
from configg import token
import logging, asyncio

bot = Bot(token=token)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


start_buttons = [
    [KeyboardButton(text='Информация'), KeyboardButton(text='Курсы')],
    [KeyboardButton(text='Адрес'), KeyboardButton(text='Контакт'), KeyboardButton(text='Соц. сети')]
  
]

start_keyboard = ReplyKeyboardMarkup(keyboard=start_buttons, resize_keyboard=True)

course_buttons = [
    [KeyboardButton(text='UI/UX'), KeyboardButton(text='Back-End'), KeyboardButton(text='Front-End')],
    [KeyboardButton(text='Назад'), KeyboardButton(text='Оставить заявку')]
]

course_keyboard = ReplyKeyboardMarkup(keyboard=course_buttons, resize_keyboard=True)


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')
    await message.answer("Если тебя интересует IT курсы, то можешь смело начать учиться в IT-Park.", reply_markup=start_keyboard)


@dp.message(F.text == "Контакт")
async def contact(message: Message):
    await message.answer_contact(first_name="IT-park", last_name=" ", phone_number='+996 704 000 705')

@dp.message(F.text == 'Адрес')
async def location(message: Message):
    await message.answer_location(latitude=40.52157915467634, longitude=72.79998740372552)


@dp.message(F.text == "Информация")
async def about(message: Message):
    await message.answer_photo(photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSF_nfZKz-Qg4e8EkCrzOPgmMkhX1jdNsLp-Q&s')
    await message.answer("IT-Park — это захватывающее путешествие в мир технологий! Здесь вы освоите программирование, дизайн, разработку. Погрузитесь в реальные проекты и найдете свой путь в IT. Учитесь, создавайте и воплощайте мечты в жизнь вместе с нами!")
    await message.answer('А также есть соц. сети IT-Park.')
    await message.answer("Какое направление IT тебя интересует?")
    await message.answer("Back-End? Front-End или UI UX?")

@dp.message(F.text == 'Соц. сети')
async def socialmedia(message: Message):
    await message.answer("Ссылка на Инстаграм - https://www.instagram.com/itpark_osh/")
    await message.answer('Ссылка на Facebook - https://www.facebook.com/237613209431104')


@dp.message(F.text == "Курсы")
async def contact(message: Message):
    await message.reply("Вот наши курсы: ", reply_markup=course_keyboard)

@dp.message(F.text =='UI/UX')
async def hello(message: Message):
    await message.answer('UI/UX — это дизайн и пользовательский опыт. UI (User Interface) создает красивый и удобный интерфейс, а UX (User Experience) заботится о том, чтобы взаимодействие с продуктом было комфортным и интуитивным.')
    
@dp.message(F.text == 'Back-End')
async def hello(message: Message):
    await message.answer('Back-End — это серверная часть разработки, которая отвечает за логику, базы данных и работу приложений «за кулисами». Здесь создаются мощные системы и API для взаимодействия с пользователями.') 
    
@dp.message(F.text == 'Front-End')
async def hello(message: Message):
    await message.answer('Front-End — это интерфейс и визуальная часть сайта или приложения. Разработчики Front-End превращают дизайнерские макеты в работающие страницы с помощью HTML, CSS и JavaScript.')  


@dp.message(F.text == 'Назад')
async def bakc(message:Message):
    await message.reply("Вы вернулись в меню: ", reply_markup=start_keyboard)



@dp.message(F.text == 'Оставить заявку')
async def get_contact(message:Message):
    button = [[KeyboardButton(text='Отправить заявку', request_contact=True)]] 
    keyboard = ReplyKeyboardMarkup(keyboard=button, resize_keyboard=True)
    await message.reply("Пожалуйста, отправьте свои контактные данные", reply_markup=keyboard)
    
@dp.message(F.contact)
async def application(message: Message):
    contact_info = (
        f'Заявка на курсы\n'
        f'Имя: {message.contact.first_name}\n'
        f'Фамилия: {message.contact.last_name}\n'
        f'Телефон: {message.contact.phone_number}\n'
        f'\nСпасибо, что оставили заявку!'
    )
    try:
        await bot.send_message(chat_id=-4598261248, text=contact_info)
        await message.answer('Вы вернулись на главное меню', reply_markup=start_keyboard)
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения: {e}")

async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())