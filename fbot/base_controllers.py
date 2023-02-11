from fbot import dp
from aiogram.types import Message, ContentTypes, CallbackQuery

from inline_buttons import get_user_auth_keyword

"""BASE CONTROLLERS"""

@dp.message_handler(commands=('start',))
async def hello(message: Message) -> Message:
    await message.answer("Najmi dyatel!", reply_markup=get_user_auth_keyword())


@dp.message_handler(commands=('test',))
async def hello(message: Message) -> Message:
    await message.reply(f'Shalom vsem VORAM!')