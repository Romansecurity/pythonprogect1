from data_base.db import cursor2, conn2
from aiogram import Router
from aiogram import F
from aiogram.types import Message


router = Router()
admin = ""

@router.message(F.text == "/admin")
async def admin_panel(message: Message):

    if message.from_user.id != admin:
        await message.answer("У вас нет доступа к файлам!")
        return
    
    cursor2.execute("SELECT * FROM reservation")
    data = cursor2.fetchall()

    text = "\n\n".join([str(row) for row in data])
    if text:
        await message.answer(text[:4000])
    else:
        await message.answer("🛑 Данные были удалены!")
