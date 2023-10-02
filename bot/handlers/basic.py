from aiogram import types
from aiogram.enums import ParseMode
from sqlalchemy.orm import sessionmaker

from db import get_auction
from bot.keyboards import get_inline_tracking_keyboard
from bot.parser import IcetradeParser
from bot.utils import receive_keyword_from_message, receive_user_from_message
from bot.messages import receive_auction_message


async def auction(message: types.Message, session: sessionmaker) -> None:
    keyword = receive_keyword_from_message(message)
    user = await receive_user_from_message(message, session)

    auction = await get_auction(keyword, user.id, session)

    keyboard = get_inline_tracking_keyboard(auction, keyword)

    parser = IcetradeParser(keyword)
    auction_list = await parser.parse()
    if auction_list:
        response_message = receive_auction_message(auction_list)
        await message.answer(
            response_message,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    else:
        await message.answer('Тендеры не найдены.')

    # if card_details.products:
    #     card_product = card_details.products[0]
    #     card_data = parser.prepare_card_product(card_product)
    #
    #     response_message = receive_article_message(article, card_data)
    #     await message.answer(
    #         response_message,
    #         reply_markup=keyboard,
    #         parse_mode=ParseMode.MARKDOWN,
    #         disable_web_page_preview=True
    #     )
    # else:
    #     await message.answer(
    #         'Товар не найден!\n'
    #         'Пожалуйста, проверьте введенный артикул товара и попробуйте еще раз.'
    #     )


async def empty(message: types.Message) -> None:
    await message.answer(
        'Неверный формат\n'
        'В запросе должно быть ключевое слово.\n'
        'Пример: АСУТП'
    )
