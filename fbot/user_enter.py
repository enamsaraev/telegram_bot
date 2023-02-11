from aiogram.types import Message, ContentTypes, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from fbot import dp
from inline_buttons import check_user_auth_keyword

"""NEW USER CREATION CONTROLLERS"""

class user(StatesGroup):
    add_name = State()
    add_password = State()
    auth_user = State()


@dp.callback_query_handler(text='new_user', state='*')
async def start_auth_for_the_new_user(callback: CallbackQuery):
    await callback.message.answer('Введите логин')
    await user.add_name.set()


@dp.message_handler(state=user.add_name, content_types=ContentTypes.TEXT)
async def add_user_nickname(message: Message, state: FSMContext) -> Message:

    user_nickname = message.text.lower()
    await state.update_data(
        user_id = message.from_user.id,
        user_nickname=user_nickname
    )
    
    await message.answer('Введите пароль: минимум - 8 символов')
    await user.add_password.set()


@dp.message_handler(state=user.add_password, content_types=ContentTypes.TEXT)
async def add_user_password(message: Message, state: FSMContext) -> Message:

    user_password = message.text.lower()
    await state.update_data(user_password=user_password)

    data = await state.get_data()
    await message.answer(f'{data}', reply_markup=check_user_auth_keyword())
    await user.auth_user.set()


@dp.callback_query_handler(text='auth_user_all_correct', state=user.auth_user)
async def user_auth(message: Message, state: FSMContext) -> Message:
    data = await state.get_data()
    await message.answer(f'{data}')
    await state.finish()