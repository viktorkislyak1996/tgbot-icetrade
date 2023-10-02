from aiogram import types
from aiogram.enums import ParseMode
from sqlalchemy.orm import sessionmaker

# from db import get_product
# from bot.keyboards import get_inline_tracking_keyboard
# from bot.parser import WBCardDetailParser
# from bot.utils import receive_article_from_message, receive_user_from_message
# from bot.messages import receive_article_message


# async def article(message: types.Message, session: sessionmaker) -> None:
#     article = receive_article_from_message(message)
#     user = await receive_user_from_message(message, session)
#
#     product = await get_product(article, user.id, session)
#
#     keyboard = get_inline_tracking_keyboard(product, article)
#
#     parser = WBCardDetailParser(article=article)
#     card_details = await parser.async_get_card_details()
#     if card_details.products:
#         card_product = card_details.products[0]
#         card_data = parser.prepare_card_product(card_product)
#
#         response_message = receive_article_message(article, card_data)
#         await message.answer(
#             response_message,
#             reply_markup=keyboard,
#             parse_mode=ParseMode.MARKDOWN,
#             disable_web_page_preview=True
#         )
#     else:
#         await message.answer(
#             'Товар не найден!\n'
#             'Пожалуйста, проверьте введенный артикул товара и попробуйте еще раз.'
#         )


async def empty(message: types.Message) -> None:
    await message.answer(
        'Неверный формат\n'
        'В запросе должно быть ключевое слово.\n'
        'Пример: АСУТП'
    )
