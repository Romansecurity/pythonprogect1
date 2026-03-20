from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from keyboards.inline import inline_start


router = Router()

text = (
    "<b>Здравствуйте!</b> 👋\n\n"
    "Этот бот поможет вам подобрать удобный зал и тренера для вашего ребёнка, "
    "а также оставить заявку на первую тренировку.\n\n"
    "Если вы не знаете, к какому тренеру записаться, нажмите <b>«Выбрать зал»</b> и "
    "мы поможем подобрать подходящего специалиста по местоположению.\n\n")
#parse_mode="HTML"

@router.message(CommandStart())
async def start_command(message: Message, command: CommandObject):
    await message.answer(text, parse_mode="HTML", reply_markup=inline_start)

