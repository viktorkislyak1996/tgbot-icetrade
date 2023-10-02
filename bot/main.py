import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from sqlalchemy import URL

# from bot.routes import register_user_commands
# from bot.scheduler import spp_price_tracker
# from bot.commands.bot_commands import bot_commands

from db import create_async_engine, get_session_maker

logger = logging.getLogger(__name__)
load_dotenv()


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    # for cmd in bot_commands:
    #     commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    dp = Dispatcher()
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))

    await bot.set_my_commands(commands=commands_for_bot)

    # register commands and handlers
    # register_user_commands(dp)

    postgres_url = URL.create(
        'postgresql+asyncpg',
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        port=os.getenv("POSTGRES_PORT"),
    )
    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)

    # scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler.add_job(spp_price_tracker, trigger='interval', minutes=5, kwargs={'bot': bot, 'session': session_maker})
    # scheduler.start()

    # drop pending message
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot, session=session_maker)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped')
