from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile, Message
from aiogram import Router
from keyboards.inline import inline_district
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import F
from data_base.models import get_trainers_by_district, get_treners_info, save_reservation
from keyboards.inline import get_back_keyboard
import os


router = Router()


class Choose(StatesGroup):
    choose_place = State()
    choose_coach = State()
    trainer_info = State()
    choose_name = State()
    phone = State()
    child_name = State()
    child_age = State()

district_mapping = {
"place_sow": 2,
"place_zhd": 4,
"place_kom": 1,
"place_levo": 6,
"place_len": 5,
"place_cent": 3,
"place_zad": 7,
"place_tepl": 8,
"place_semiluki": 9,
"place_strelitsa": 10,
"place_orlov_log": 11,
"place_devitsa": 12,
"place_hoholskiy": 13
}




@router.callback_query(F.data == "choose_place")
async def choose_place_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Choose.choose_place)
    await call.message.answer("Какой район города вас интересует?", reply_markup=inline_district)
    await call.answer()

#choose place
@router.callback_query(lambda m: m.data.startswith("place_"))
async def choose_trainer_callback(call: CallbackQuery, state: FSMContext):
    

    district_id = district_mapping.get(call.data)
    if district_id is None:
        await call.answer("Ошибка:Район не найден")
        return
    
    trainers = get_trainers_by_district(district_id)

    inline_treners = InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f'trainer_{tid}_{district_id}')]
        for tid, name in trainers
        ]
    )

    await state.set_state(Choose.choose_coach)

    await call.message.delete()

    await call.message.answer("Список тренеров:", reply_markup=inline_treners)
    await call.answer()



#choose coaches
@router.callback_query(lambda c: c.data.startswith("trainer_"))
async def trainer_callback(call: CallbackQuery, state: FSMContext):

    data = call.data.split("_")

    trainer_id = int(data[1])
    district_id = int(data[2])

    trainers = get_treners_info(trainer_id, district_id)

    name = trainers[0][0]
    phone = trainers[0][1]
    addresses = "\n".join([t[2] for t in trainers])

    await state.update_data(trainer_name=name)

    caption = (
        f"<b>{name}</b>\n\n"
        f"📞 Телефон: {phone}\n\n"
        f"📍 Адреса:\n{addresses}"
    )
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # папка, где лежит callbacks.py
    photo_path = os.path.join(BASE_DIR, '..', 'photos', f'{trainer_id}.JPG')
    

    
    if not os.path.exists(photo_path):
        await call.answer("❌ Фото тренера не найдено")

        await call.message.edit_text(
            "Анкета тренера отсутствует, но запись на занятия доступна ✔︎",
            reply_markup=get_back_keyboard(district_id)
        )
        await state.set_state(Choose.trainer_info)
        return
    
    photo = FSInputFile(photo_path)
    
    await state.set_state(Choose.trainer_info)

    await call.message.delete()

    
    await call.message.answer_photo(
        photo=photo,
        caption=caption,
        parse_mode="HTML",
        reply_markup=get_back_keyboard(district_id)
    )

    await call.answer()

#back to the coaches
@router.callback_query(F.data.startswith("back_"))
async def back_coaches(call: CallbackQuery, state: FSMContext):

    data = call.data.split("_")

    district_id = int(data[1])

    trainers = get_trainers_by_district(district_id)

    inline_treners = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=name,
                callback_data=f'trainer_{tid}_{district_id}'
            )]
            for tid, name in trainers
        ] + [
        [InlineKeyboardButton(
            text="🔙 Назад к выбору района",
            callback_data=f"place2_{district_id}"
        )]
    ]
)
    

    await state.set_state(Choose.choose_coach)

    await call.message.delete()

    await call.message.answer(
        "Список тренеров:",
        reply_markup=inline_treners
    )
    await call.answer()



# back place
@router.callback_query(F.data.startswith("place2_"))
async def back_place(call: CallbackQuery, state: FSMContext):
    await state.set_state(Choose.choose_place)
    await call.message.delete()
    await call.message.answer("Какой район города вас интересует?", reply_markup=inline_district)
    await call.answer()

#reservation
@router.callback_query(F.data == "reservation")
async def reservation(call: CallbackQuery, state: FSMContext):
    await state.set_state(Choose.choose_name)
    await call.message.answer("💬Введите ваше имя и фамилию:")
    await call.answer("Начинаем бронирование!")


#name
@router.message(Choose.choose_name)
async def choose_name_last(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Choose.phone)
    await message.answer("📞Введите номер телефона:")

#phone
@router.message(Choose.phone)
async def choose_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(Choose.child_name)
    await message.answer("🧑‍🧑‍🧒Введите имя вашего ребенка:")

#name child
@router.message(Choose.child_name)
async def choose_child_name(message: Message, state: FSMContext):
    await state.update_data(n_child=message.text)
    await state.set_state(Choose.child_age)
    await message.answer("🧑‍🧑‍🧒Введите возраст вашего ребенка:")

#name age
@router.message(Choose.child_age)
async def choose_child_name(message: Message, state: FSMContext):
    await state.update_data(a_child=message.text)
    data = await state.get_data()


    text = (
        f"✅ Анкета заполнена:\n\n"
        f"👤 {data.get('name','Не указано')}\n"
        f"📱 {data.get('phone','Не указано')}\n"
        f"👶 {data.get('n_child','Не указано')}\n"
        f"🎂 {data.get('a_child','Не указано')} лет\n"
        f"Тренер: {data.get('trainer_name','Не указан')}"
    )

    save_reservation(data)

    await message.answer("Благодарим за заявку! В ближайшее время " \
    "наш секретарь свяжется\n" \
    "с вами для подтверждения записи 🤝")

    await state.clear()
    print(text)

 


