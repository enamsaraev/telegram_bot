import os
import requests

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()


API_TOKEN = os.environ.get('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=('start',))
async def hello(message: Message) -> Message:
    await message.reply(f'Start!')


@dp.message_handler(commands=('test',))
async def hello(message: Message) -> Message:
    await message.reply(f'Shalom vsem VORAM!')


"""CATEGORIES CONTROLLERS"""

class category(StatesGroup):
    add_category = State()
    add_aliases = State()


@dp.message_handler(commands='add_category', state='*')
async def add_func(message: Message, state: FSMContext) -> Message:
    await message.answer('EHALA!')
    await message.answer(f"Введите категорию трат, например <еда>")
    await category.add_category.set()


@dp.message_handler(state=category.add_category, content_types=ContentTypes.TEXT)
async def add_func(message: Message, state: FSMContext) -> Message:

    user_category = message.text.lower()
    await state.update_data(category=user_category)
    
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


@dp.message_handler(commands=('get_categories',))
async def shau(message: Message, state: FSMContext):

    res = requests.get('http://127.0.0.1:8000/api/get_categories/')
    data = res.json()['msg']
    msg = '\n'.join([f'{key.capitalize()}: {value}' for key, value in data[0].items()])
    await message.answer(msg)


"""EXPENSES CONTROLLERS"""

class expense(StatesGroup):
    add = State()


@dp.message_handler(commands='add_expense', state='*')
async def add_func(message: Message, state: FSMContext) -> Message:
    await message.reply(f"Введите текущую трату, например <550 еда>")
    await expense.add.set()


@dp.message_handler(state=expense.add, content_types=ContentTypes.TEXT)
async def shau(message: Message, state: FSMContext):
    data = {
        'msg_text':str(message.text)
    }
    res = requests.post('http://127.0.0.1:8000/api/add_expense/', data=data)
    await message.answer(f'{res.json()["msg"]}')
    await state.finish()