from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from database import cursor, connection
from schedule import get_juz_keyboard, send_user_table

router = Router()

@router.message(Command('start'))
async def start_bot(msg : Message):
    await msg.answer('السلام عليكم')
    cursor.execute("SELECT * FROM users where telegram_id = ?", (msg.from_user.id,))
    row = cursor.fetchone()
    if row:   
        await msg.answer("Параны алып алу үшін, /juz жазыңыз")
    else:
        await msg.answer('/registration жазыңыз!')

@router.message(Command('excel'))
async def send_excel(msg : Message):
    await send_user_table()
    await msg.answer('Excel жіберілді!')

@router.message(Command('juz'))
async def free_juz(msg : Message):
    cursor.execute("SELECT * FROM users where telegram_id = ?", (msg.from_user.id,))
    row = cursor.fetchone()
    if row:
        cursor.execute('SELECT juz FROM users where telegram_id = ?', (msg.from_user.id))
        ans = cursor.fetchone()
        if ans:
            await msg.answer(f"Сіз {ans.get('juz')} таңдап алғансыз!")
        else:
            await msg.answer('Оқитын параны таңдаңыз!', reply_markup=get_juz_keyboard())
    else:
        await msg.answer("Біріншіден /registration жазыңыз!")

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