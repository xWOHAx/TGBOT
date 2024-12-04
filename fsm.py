from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config3 import token
import asyncio, logging, sqlite3


logging.basicConfig(level=logging.INFO)


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


connection = sqlite3.connect('fsm.db')
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER,
        username TEXT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    )
""")


class Form(StatesGroup):
    name = State()
    age = State()
    photo = State()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.reply('Здравствуйте! Как вас зовут?')


@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer('Сколько вам лет?')


@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Пожалуйста, введите корректный возраст.')
        return

    age = int(message.text)
    if age < 18:
        await state.clear()
        await message.answer('Доступ запрещён для несовершеннолетних!')
        return


    data = await state.get_data()
    name = data.get('name')

    try:
        connection = sqlite3.connect('fsm.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO users (id, username, name, age)
            VALUES (?, ?, ?, ?)
        """, (message.from_user.id, message.from_user.username, name, age))
        connection.commit()
        connection.close()
    except Exception as e:
        logging.error(f"Ошибка сохранения в базу данных: {e}")
        await message.answer('Ошибка при сохранения в базу данных.')
        return



    await state.update_data(age=age)
    await state.set_state(Form.photo)
    await message.answer("Отправьте мне свою фотографию")


@dp.message(Form.photo, F.content_type.in_(['photo']))
async def process_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    name = data.get('name')
    age = data.get('age')
    photo = message.photo[-1].file_id
   
    await bot.send_message(
        message.chat.id,
        f'Твое имя: {name}\nТвой возраст: {age}',
    )
    
    await bot.send_photo(message.chat.id, photo)
    await state.clear()
    await message.answer(f'Ваши данные сохранены.')



@dp.message(Command('cancel'))
@dp.message(F.text.lower() == 'отмена')
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Процесс отменён. Для начала нового процесса отправьте команду /start.')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())