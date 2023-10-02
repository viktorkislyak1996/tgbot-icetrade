# import os
#
# from aiogram.enums import ParseMode
# from aiogram.types import CallbackQuery
# from aiogram.utils.markdown import link
# from dotenv import load_dotenv
# from sqlalchemy.orm import sessionmaker
#
# from bot.db import (
#     create_product,
#     get_product,
#     update_product,
#     get_products_count,
#     delete_product
# )
# from bot.keyboards import (
#     get_inline_tracking_keyboard,
#     get_inline_stop_tracking_keyboard,
#     get_inline_run_tracking_keyboard
# )
# from bot.parser import WBCardDetailParser
# from bot.utils import receive_article_from_callback, receive_user_from_message
# from bot.messages import receive_article_message
#
# load_dotenv()
#
#
# async def run_tracking_callback(callback: CallbackQuery, session: sessionmaker) -> None:
#     article = receive_article_from_callback(callback)
#     user = await receive_user_from_message(callback, session)
#
#     keyboard = get_inline_run_tracking_keyboard(article)
#     article_link = link(f'{article}', f'https://www.wildberries.ru/catalog/{article}/detail.aspx')
#
#     parser = WBCardDetailParser(article=article)
#     card_details = await parser.async_get_card_details()
#     if card_details.products:
#         card_product = card_details.products[0]
#         card_data = parser.prepare_card_product(card_product)
#
#         product = await get_product(article, user.id, session)
#         if not product:
#             products_count = await get_products_count(user.id, session)
#             products_count_limit = int(os.getenv('PRODUCTS_COUNT_LIMIT', 50))
#             if products_count > products_count_limit:
#                 await callback.message.answer(
#                     f'Лимит отслеживаемых товаров (*{products_count_limit}*) превышен!\n'
#                     f'Чтобы начать отслеживание по товару, выключите отслеживания на каком-либо другом вашем товаре.',
#                     parse_mode=ParseMode.MARKDOWN,
#                     disable_web_page_preview=True
#                 )
#                 return
#
#             product_data = {
#                 'wb_id': card_data['wb_id'],
#                 'user_id': user.id,
#                 'name': card_data['name'],
#                 'brand': card_data['brand'],
#                 'region': 'Москва',
#                 'price_without_discount': card_data['price_without_discount'],
#                 'price_with_discount': card_data['price_with_discount'],
#                 'price_for_users': card_data['price_for_users'],
#                 'discount': card_data['discount'],
#                 'remains': card_data['remains'],
#                 'is_spp': card_data['is_spp'],
#                 'spp': card_data['spp'],
#                 'tracking': True
#             }
#             await create_product(product_data, session)
#         else:
#             update_product_data = {'tracking': True}
#             await update_product(product, update_product_data, session)
#
#         await callback.message.answer(
#             f'Отслеживание товара {article_link} включено!',
#             reply_markup=keyboard,
#             parse_mode=ParseMode.MARKDOWN,
#             disable_web_page_preview=True
#         )
#     else:
#         await callback.message.answer(
#             'Что-то пошло не так! \n '
#             'Пожалуйста, подождите несколько минут и повторите попытку.'
#         )
#
#
# async def stop_tracking_callback(callback: CallbackQuery, session: sessionmaker) -> None:
#     article = receive_article_from_callback(callback)
#     user = await receive_user_from_message(callback, session)
#
#     keyboard = get_inline_stop_tracking_keyboard(article)
#
#     product = await get_product(article, user.id, session)
#
#     article_link = link(f'{article}', f'https://www.wildberries.ru/catalog/{article}/detail.aspx')
#     if product:
#         await delete_product(product, session)
#
#         await callback.message.answer(
#             f'Отслеживание товара {article_link} выключено',
#             reply_markup=keyboard,
#             parse_mode=ParseMode.MARKDOWN,
#             disable_web_page_preview=True
#         )
#     else:
#         await callback.message.answer(
#             f'Продукт {article_link} не найден!\n'
#             f'Пожалуйста, повторите запрос или обратитесь к администратору',
#             parse_mode=ParseMode.MARKDOWN,
#             disable_web_page_preview=True
#         )
#
#
# async def refresh_callback(callback: CallbackQuery, session: sessionmaker) -> None:
#     article = receive_article_from_callback(callback)
#     user = await receive_user_from_message(callback, session)
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
#         await callback.message.answer(
#             response_message,
#             reply_markup=keyboard,
#             parse_mode=ParseMode.MARKDOWN,
#             disable_web_page_preview=True
#         )
#     else:
#         await callback.message.answer(
#             'Что-то пошло не так! \n '
#             'Пожалуйста, подождите несколько минут и повторите попытку.'
#         )
