from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup ,WebAppInfo
from data_base.models import get_trainers_by_district

inline_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать зал", callback_data='choose_place')],
        [InlineKeyboardButton(text="Открыть карту",  web_app=WebAppInfo(url="https://yandex.ru/maps/193/voronezh/?from=mapframe&ll=39.241019%2C51.669204&mode=usermaps&source=mapframe&um=constructor%3A36bfa1e04e6186ca5a529863a485dba549cb19d456f70287cd2e8f903a7466aa&utm_source=mapframe&z=11.83"))]
    ]
)

inline_district = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Советский район", callback_data='place_sow')],
        [InlineKeyboardButton(text="Железнодородный район", callback_data='place_zhd')],
        [InlineKeyboardButton(text="Коминтерновский район", callback_data='place_kom')],
        [InlineKeyboardButton(text="Левобережный район", callback_data='place_levo')],
        [InlineKeyboardButton(text="Ленинский район", callback_data='place_len')],
        [InlineKeyboardButton(text="Центральный район", callback_data='place_cent')],
        [InlineKeyboardButton(text="Жилой массив Задонье", callback_data='place_zad')],
        [InlineKeyboardButton(text="п.Тепличный", callback_data='place_tepl')],
        [InlineKeyboardButton(text="г.Семилуки", callback_data='place_semiluki')],
        [InlineKeyboardButton(text="с.Стрелица", callback_data='place_strelitsa')],
        [InlineKeyboardButton(text="пос. Орлов лог", callback_data='place_orlov_log')],
        [InlineKeyboardButton(text="с.Девица", callback_data='place_devitsa')],
        [InlineKeyboardButton(text="Хохольский район", callback_data='place_hoholskiy')],
    ]
)


def get_back_keyboard(district_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад к тренерам данного района", callback_data=f'back_{district_id}')],
            [InlineKeyboardButton(text="🏠 Назад к выбору района", callback_data='place2_')],
            [InlineKeyboardButton(text="✅ Записаться на занятие", callback_data='reservation')]
        ]
    )


inline_back = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Назад к выбору района", callback_data='back2')],
    ]
)