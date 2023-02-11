from aiogram.types import Message, ContentTypes, CallbackQuery
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from fbot import dp


"""INLINE BUTTONS"""

def get_menu_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text='Посмотреть все категории', callback_data='all_categories'),
        ],
        [
            InlineKeyboardButton(text='Добавить категорию', callback_data='add_category'),
            InlineKeyboardButton(text='Добавить трату', callback_data='add_expense'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_user_auth_keyword():
    buttons = [
        [
            InlineKeyboardButton(text='Я новый пользователь', callback_data='new_user'),
            InlineKeyboardButton(text='Я уже есть', callback_data='current_user'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def check_user_auth_keyword():
    buttons = [
        [
            InlineKeyboardButton(text='Все верно', callback_data='auth_user_all_correct'),
            InlineKeyboardButton(text='Ввести заново', callback_data='new_user'),
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


"""INLINE BUTTONS CONTROLLERS"""

@dp.message_handler(commands=['menu'])
async def menu(message: Message):
    await message.reply("Najmi dyatel!", reply_markup=get_menu_keyboard())


@dp.callback_query_handler(text='test_cb')
async def test(callback: CallbackQuery):
    await callback.message.answer('zaschitano!')