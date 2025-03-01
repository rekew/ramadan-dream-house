from datetime import datetime
from database import cursor, connection, get_taken_juz, get_users, clear_user_table
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from config import bot
import pandas as pd
import asyncio
import pytz
import os

ALMATY_TZ = pytz.timezone("Asia/Almaty") 

async def send_user_table():
    excel_file = 'users.xlsx'
    if os.path.exists(excel_file):
        os.remove(excel_file)
    df = pd.read_sql('SELECT * FROM users', connection)
    df.to_excel(excel_file, index=False, engine='openpyxl')
    ADMIN_CHAT_ID = 877873893
    await bot.send_document(ADMIN_CHAT_ID, FSInputFile(excel_file))

def get_juz_keyboard():
    taken_juz = get_taken_juz()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Juz {i}", callback_data=f"select_juz_{i}")]
        for i in range(1, 31) if str(i) not in taken_juz  
    ])
    return keyboard

async def send_juz_selection():
    while True:
        now = datetime.now(ALMATY_TZ)
        if now.hour == 4:
            users = get_users()
            for user_id in users:
                try:
                    await bot.send_message(user_id, 'Выберите джуз для чтения:', reply_markup=get_juz_keyboard())
                except Exception as e:
                    print(f"Ошибка при отправке {user_id}: {e}")
            await send_user_table()
            clear_user_table()
            await asyncio.sleep(3601)
        await asyncio.sleep(60)

async def send_scheduled_message():
    while True:
        now = datetime.now(ALMATY_TZ)
        if now.hour == 20:
            users = get_users()
            for user_id in users:
                try:
                    kb = InlineKeyboardMarkup(inline_keyboard = [
                        [InlineKeyboardButton(text = 'Біттім', callback_data='done_Quran')],
                        [InlineKeyboardButton(text = 'Бітпедім', callback_data='notDone_Quran')]
                    ])
                    await bot.send_message(user_id, 'Құранды біттіңіз ба?', reply_markup=kb)
                except Exception as e:
                    print(f"Ошибка при отправке {user_id}: {e}")
            await asyncio.sleep(3601)
        await asyncio.sleep(60)