from aiogram import types
from aiogram.enums import ParseMode

from bot.keyboards import get_reply_tracking_keywords_keyboard


async def start(message: types.Message) -> None:
    keyboard = get_reply_tracking_keywords_keyboard()
    await message.answer(
        'Введите ключевое слово, которое вас интересует, и  получите информацию о закупках.\n'
        'Пример: *АСКУЭ*',
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )
