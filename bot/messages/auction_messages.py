from aiogram.utils.markdown import link

from bot.scraper import AuctionTable
from bot.utils import digit_to_emoji
from db import Auction


def receive_parsed_message(auction_list: list[AuctionTable], title: str) -> str:
    response_message = (
        title
    )
    for index, auction in enumerate(auction_list, start=1):
        auction_link = link(f'Ссылка на тендер', f'{auction.link}')
        response_message += (
            f'{digit_to_emoji[index]} Краткое описание: *{auction.description}*\n'
            f'{digit_to_emoji[index]} Наименование заказчика: *{auction.customer_name}*\n'
            f'{digit_to_emoji[index]} Номер: *{auction.number}*\n'
            f'🌎 Страна: *{auction.country}*\n'
            f'💰 Стоимость: *{auction.cost}*\n'
            f'⏳ Действует до: *{auction.expires_at}*\n'
            f'➡️ {auction_link}\n\n\n'
        )
    return response_message


def receive_db_auction_message(auction: Auction) -> str:
    auction_link = link(f'Ссылка на тендеры', f'{auction.link}')
    last_updated = auction.updated_at if auction.updated_at else auction.created_at
    response_message = (
        f'📌 Ключевое слово: *{auction.keyword}*\n\n'
    )
    if auction.offers_number:
        response_message += (
            f'✅ Количество тендеров: *{auction.offers_number}*\n'
        )
    else:
        response_message += (
            f'❌ *Тендеры не найдены*\n'
        )
    response_message += (
        f'⏱ Обновление: *{last_updated.strftime("%d.%m.%Y")}*\n\n'
        f'➡️ {auction_link}\n'
    )
    return response_message


def receive_parsed_auction_message(auction_list: list[AuctionTable], keyword: str) -> str:
    title = f'🔎 *{keyword}*\n\n'
    message = receive_parsed_message(auction_list, title)
    return message


def receive_not_found_auction_message(keyword: str) -> str:
    response_message = (
        f'🔎 *{keyword}*\n\n'
        f'❌ *Тендеры не найдены*\n'
    )
    return response_message


def receive_parsed_scheduler_message(auction_list: list[AuctionTable], keyword: str) -> str:
    title = (
        f'🔥 *Появились новые тендеры!*\n\n'
        f'📌 Ключевое слово: *{keyword}*\n\n'
    )
    message = receive_parsed_message(auction_list, title)
    return message
