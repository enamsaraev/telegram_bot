import logging

from aiogram import executor

from fbot.fbot import dp
# from fbot.base_controllers import dp
# from fbot.inline_buttons import dp
# from fbot.user_enter import dp


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    executor.start_polling(dp)