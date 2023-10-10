from aiogram import types
from aiogram.enums import ParseMode
from sqlalchemy.orm import sessionmaker

from db import get_auction
from bot.keyboards import get_inline_tracking_keyboard
from bot.scraper import IcetradeScraper
from bot.utils import receive_keyword_from_message, receive_user_from_message
from bot.messages import receive_parsed_auction_message, receive_not_found_auction_message


async def auction(message: types.Message, session: sessionmaker) -> None:
    keyword = receive_keyword_from_message(message)
    if len(keyword) > 25:
        await message.answer(
            'Длина ключевого слова не должна превышать *25* символов!\n'
            'Пожалуйста, умерьте свой аппетит\n',
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    if not keyword:
        await message.answer(
            'Неверный формат\n'
            'В запросе должно быть ключевое слово.\n'
            'Пример: *АСУТП*',
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    user = await receive_user_from_message(message, session)
    auction = await get_auction(keyword, user.id, session)
    keyboard = get_inline_tracking_keyboard(auction, keyword)

    parser = IcetradeScraper(keyword)
    auction_list = await parser.get_auction()
    if auction_list:
        response_message = receive_parsed_auction_message(auction_list, keyword)
    else:
        response_message = receive_not_found_auction_message(keyword)

    await message.answer(
        response_message,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


async def empty(message: types.Message) -> None:
    await message.answer(
        'Неверный формат\n'
        'В запросе должно быть ключевое слово.\n'
        'Пример: АСУТП'
    )
