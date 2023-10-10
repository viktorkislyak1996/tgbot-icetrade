import os

from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

from db import (
    create_auction,
    update_auction,
    delete_auction,
    get_auction,
    get_keywords_count
)
from bot.keyboards import (
    get_inline_tracking_keyboard,
    get_inline_stop_tracking_keyboard,
    get_inline_run_tracking_keyboard
)
from bot.scraper import IcetradeScraper
from bot.utils import receive_keyword_from_callback, receive_user_from_message
from bot.messages import receive_parsed_auction_message, receive_not_found_auction_message

load_dotenv()


async def run_tracking_callback(callback: CallbackQuery, session: sessionmaker) -> None:
    keyword = receive_keyword_from_callback(callback)
    user = await receive_user_from_message(callback, session)

    keyboard = get_inline_run_tracking_keyboard(keyword)

    parser = IcetradeScraper(keyword)
    auction_info = await parser.get_auction_info()
    auction = await get_auction(keyword, user.id, session)
    if not auction:
        keywords_count = await get_keywords_count(user.id, session)
        keywords_count_limit = int(os.getenv('KEYWORDS_COUNT_LIMIT', 20))
        if keywords_count > keywords_count_limit:
            await callback.message.answer(
                f'Лимит отслеживаемых ключевых слов (*{keywords_count_limit}*) превышен!\n'
                f'Чтобы начать новое отслеживание, выключите отслеживания какого-либо другого ключевого слова.',
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return

        auction_data = {
            'user_id': user.id,
            'keyword': keyword,
            'tracking': True,
            'link': auction_info.get('auction_link')
        }
        if last_tender := auction_info.get('last_tender'):
            auction_data.update(
                {
                    'offers_number': auction_info['offers_number'],
                    'number': last_tender.number
                }
            )
        await create_auction(auction_data, session)
    else:
        update_auction_data = {'tracking': True}
        if not auction_info.get('last_tender'):
            update_auction_data.update(
                {
                    'offers_number': None,
                    'number': None
                }
            )
        await update_auction(auction, update_auction_data, session)

    await callback.message.answer(
        f'Отслеживание тендеров по ключевому слову *{keyword}* включено!',
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


async def stop_tracking_callback(callback: CallbackQuery, session: sessionmaker) -> None:
    keyword = receive_keyword_from_callback(callback)
    user = await receive_user_from_message(callback, session)

    keyboard = get_inline_stop_tracking_keyboard(keyword)

    auction = await get_auction(keyword, user.id, session)
    if auction:
        await delete_auction(auction, session)

        await callback.message.answer(
            f'Отслеживание тендеров по ключевому слову *{keyword}* выключено!',
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    else:
        await callback.message.answer(
            f'Тендеры по ключевому слову *{keyword}* не найден!\n'
            f'Пожалуйста, повторите запрос или обратитесь к администратору',
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )


async def refresh_callback(callback: CallbackQuery, session: sessionmaker) -> None:
    keyword = receive_keyword_from_callback(callback)
    user = await receive_user_from_message(callback, session)

    auction = await get_auction(keyword, user.id, session)

    keyboard = get_inline_tracking_keyboard(auction, keyword)

    parser = IcetradeScraper(keyword)
    auction_list = await parser.get_auction()
    if auction_list:
        response_message = receive_parsed_auction_message(auction_list, keyword)
    else:
        response_message = receive_not_found_auction_message(keyword)

    await callback.message.answer(
        response_message,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

