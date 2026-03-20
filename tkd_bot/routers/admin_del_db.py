from data_base.db import cursor2, conn2
from aiogram import Router
from aiogram import F
from aiogram.types import Message


router = Router()
admin = 2020925154

@router.message(F.text == "/delete")
async def admin_delete(message: Message):

    if message.from_user.id != admin:
        await message.answer("У вас нет доступа к файлам!")
        return
    
    cursor2.execute("""DELETE FROM reservation""")
    cursor2.execute("""DELETE FROM sqlite_sequence WHERE name='reservation' """)
    conn2.commit()

    await message.answer("🗑 База очищена!")
    