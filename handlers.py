from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from database import cursor, connection

router = Router()

@router.message(Command('start'))
async def start_bot(msg : Message):
    await msg.answer('السلام عليكم')
    await msg.answer('/registration жазыңыз!')

@router.message(Command('registration'))
async def registration(msg : Message):
    user_id = msg.from_user.id
    cursor.execute("SELECT * FROM users where telegram_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        await msg.answer("Сіз базада барсыз!")
    else:
        username = msg.from_user.username
        cursor.execute('''
            INSERT INTO users(telegram_id, username) VALUES(?, ?)
        ''', (user_id, username))
        connection.commit()
        await msg.answer("Сізді базаға енгіздім")