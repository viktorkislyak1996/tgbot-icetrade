from aiogram import Router, F
from aiogram.filters.command import CommandStart
from aiogram.filters import Command

from bot.commands import start, help, keywords
from bot.handlers import empty, auction


def register_user_commands(router: Router) -> None:
    router.message.register(start, CommandStart())
    router.message.register(help, Command(commands=['help']))
    router.message.register(auction, F.text)

    router.message.register(keywords, Command(commands=['keywords']))
    router.message.register(keywords, F.text == 'Отслеживаемые ключевые слова')
    #
    # router.callback_query.register(run_tracking_callback, F.data.startswith('run_tracking_'))
    # router.callback_query.register(stop_tracking_callback, F.data.startswith('stop_tracking_'))
    # router.callback_query.register(refresh_callback, F.data.startswith('refresh_'))

    router.message.register(empty)
