from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config2 import token
import logging, asyncio, time, sqlite3


bot = Bot(token=token)
dp = Dispatcher()


logging.basicConfig(level=logging.INFO)


connection = sqlite3.connect('notes.db')
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INT,
        first_name VARCHAR(25),
        last_name VARCHAR (25),
        username VARCHAR (25),
        created VARCHAR (25)
);
""")


@dp.message(CommandStart())
async def start(message: Message):
    cursor.execute("SELECT id FROM users WHERE id = ?", (message.from_user.id,))
    user_result = cursor.fetchall()
    print(user_result)
    if user_result == []:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?); ",
                   (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, time.ctime()))
    cursor.connection.commit()
    await message.answer(f'Привет, {message.from_user.full_name}!')
    await message.answer("Список всех студентов: ")
    cursor.execute("""
        SELECT 
            ROW_NUMBER() OVER (ORDER BY id) as row_num,
            first_name, 
            last_name, 
            username 
        FROM users
    """)
    students = cursor.fetchall()

    student_list = "\n".join(
        [f"{student[0]}. {student[1]} {student[2]})" for student in students]
)
    await message.answer("Список всех студентов:\n" + student_list)


    
    # cursor.execute("SELECT * FROM users WHERE id = ?", (message.from_user.first_name,))
    # students = cursor.fetchall()
    # await message.answer(students)




@dp.message(Command('delete'))
async def delete(message: Message):
    cursor.execute("DELETE FROM users WHERE id = ?", (message.from_user.id,))
    cursor.connection.commit()
    await message.answer(f"Вы, {message.from_user.id}, были успешно удалены")





async def main():
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())