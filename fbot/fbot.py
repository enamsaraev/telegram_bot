import os
import requests

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentTypes, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()


API_TOKEN = os.environ.get('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


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
            InlineKeyboardButton(text='Я уже есть', callback_data='new_user'),
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


"""BASE CONTROLLERS"""

@dp.message_handler(commands=('start',))
async def hello(message: Message) -> Message:
    await message.answer("Najmi dyatel!", reply_markup=get_user_auth_keyword())


@dp.message_handler(commands=('test',))
async def hello(message: Message) -> Message:
    await message.reply(f'Shalom vsem VORAM!')


"""NEW USER CREATION CONTROLLERS"""

class user(StatesGroup):
    add_name = State()
    add_password = State()
    auth_user = State()


@dp.callback_query_handler(text='new_user', state='*')
async def start_auth_for_the_new_user(callback: CallbackQuery):
    await callback.message.answer('Введите email')
    await user.add_name.set()


@dp.message_handler(state=user.add_name, content_types=ContentTypes.TEXT)
async def add_user_nickname(message: Message, state: FSMContext) -> Message:

    user_email = message.text.lower()

    await state.update_data(
        user_id = message.from_user.id,
        user_email=user_email
    )
    
    await message.answer('Введите пароль: минимум - 8 символов')
    await user.add_password.set()


@dp.message_handler(state=user.add_password, content_types=ContentTypes.TEXT)
async def add_user_password(message: Message, state: FSMContext) -> Message:

    user_password = message.text.lower()
    if len(user_password) < 8:
        await message.answer('Введите пароль: минимум - 8 символов')
    
    else:
        await state.update_data(user_password=user_password)

        data = await state.get_data()
        msg = '\n'.join([
            f"Email: {data['user_email']}",
            f"Пароль: {data['user_password']}"
        ])
        await message.answer(msg, reply_markup=check_user_auth_keyword())
        await user.auth_user.set()


@dp.callback_query_handler(text='auth_user_all_correct', state=user.auth_user)
async def user_auth(callback: CallbackQuery, state: FSMContext) -> Message:
    state_data = await state.get_data()
    data = {
        'user_chat_id': state_data['user_id'],
        'user_email': state_data['user_email'],
        'user_password': state_data['user_password']
    }

    await state.finish()

    res = requests.post('http://127.0.0.1:8000/api/registration/', data=data)
    
    if res.status_code != 200:
        await callback.message.answer('Данные авторизации неверны', reply_markup=get_user_auth_keyword())

    else:
        await callback.message.answer('Меню:', reply_markup=get_menu_keyboard())

    
"""CATEGORIES CONTROLLERS"""

class category(StatesGroup):
    add_category = State()
    add_aliases = State()


@dp.callback_query_handler(text='all_categories')
async def shau(callback: CallbackQuery, state: FSMContext):
    res = requests.get('http://127.0.0.1:8000/api/get_categories/', data={'user_chat_id': callback.from_user.id})
    data = res.json()['msg']

    if data[0]:
        msg = '\n'.join([f'{key.capitalize()}: {value}' for key, value in data[0].items()])
        await callback.message.answer(msg)
    else:
        await callback.message.answer('У вас пока нет добавленных категорий ')


@dp.callback_query_handler(text='add_category', state='*')
async def add_func(callback: CallbackQuery, state: FSMContext) -> Message:
    await callback.message.answer('EHALA!')
    await callback.message.answer(f"Введите категорию трат, например <еда>")
    await category.add_category.set()


@dp.message_handler(state=category.add_category, content_types=ContentTypes.TEXT)
async def add_func(message: Message, state: FSMContext) -> Message:

    user_category = message.text.lower()
    await state.update_data(
        user_chat_id=message.from_user.id,
        category=user_category
    )
    
    await message.answer(f"Введите ключевые слова категории трат: \
                        например, если категория трат - еда <хлеб, молоко, шоколад>")
    await category.add_aliases.set()


@dp.message_handler(state=category.add_aliases, content_types=ContentTypes.TEXT)
async def add_func(message: Message, state: FSMContext) -> Message:
    
    user_category_aliases = message.text.lower()

    await state.update_data(category_aliases=user_category_aliases)
    await message.answer('JI ES')

    data = await state.get_data()
    await state.finish()

    res = requests.post('http://127.0.0.1:8000/api/add_category/', data=data)
    await message.answer(f'{res.json()["msg"]}')


"""EXPENSES CONTROLLERS"""

class expense(StatesGroup):
    add = State()

@dp.callback_query_handler(text='add_expense', state='*')
async def add_func(callback: CallbackQuery, state: FSMContext) -> Message:
    await callback.message.reply(f"Введите текущую трату, например <550 еда>")
    await expense.add.set()


@dp.message_handler(state=expense.add, content_types=ContentTypes.TEXT)
async def shau(message: Message, state: FSMContext):
    data = {
        'user_chat_id': message.from_user.id,
        'msg_text':str(message.text)
    }
    res = requests.post('http://127.0.0.1:8000/api/add_expense/', data=data)
    await message.answer(f'{res.json()["msg"]}')
    await state.finish()