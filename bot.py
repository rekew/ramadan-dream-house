from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from database import cursor, connection, get_taken_juz
from schedule import send_juz_selection, send_scheduled_message
from handlers import router
from config import bot
import asyncio
#asd

dp = Dispatcher()

@router.callback_query(F.data == 'done_Quran')
async def QuranDone(call : CallbackQuery):
    await call.message.answer('Красапчиксіз ғой')
    cursor.execute('''
        INSERT INTO users (telegram_id, quran_mark)
        VALUES (?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
        quran_mark = excluded.quran_mark
    ''', (call.from_user.id, True))
    connection.commit()
    await call.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data == 'notDone_Quran')
async def QuranNotDone(call : CallbackQuery):
    await call.message.answer("Эххх емае")
    cursor.execute('''
        INSERT INTO users (telegram_id, quran_mark)
        VALUES (?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
        quran_mark = excluded.quran_mark
    ''', (call.from_user.id, False))
    connection.commit()
    await call.message.edit_reply_markup(reply_markup=None)

@router.callback_query(F.data.startswith("select_juz_"))
async def select_juz(call: CallbackQuery):
    juz_number = call.data.split("_")[-1] 

    if juz_number in get_taken_juz():
        await call.message.answer(f"❌ Джуз {juz_number} уже занят. Выберите другой.")
        return
    cursor.execute('''
        INSERT INTO users (telegram_id, juz)
        VALUES (?, ?)
        ON CONFLICT(telegram_id) DO UPDATE SET
        juz = excluded.juz
    ''', (call.from_user.id, juz_number))

    connection.commit()
    await call.message.answer(f"✅ Вы выбрали Juz {juz_number}!")
    await call.message.edit_reply_markup(reply_markup=None)

async def main():
    try:
        asyncio.create_task(send_scheduled_message())
        asyncio.create_task(send_juz_selection())
        dp.include_router(router)
        await dp.start_polling(bot)
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    asyncio.run(main())