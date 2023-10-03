from aiogram.utils.markdown import link

from bot.parser import AuctionTable
from bot.utils import digit_to_emoji
from db import Auction


def receive_db_auction_message(auction: Auction) -> str:
    auction_link = link(f'Ссылка на аукцион', f'{auction.link}')
    last_updated = auction.updated_at if auction.updated_at else auction.created_at
    response_message = (
        f'🚀*Icetrade_bot*\n\n'
        f'📌 Ключевое слово: *{auction.keyword}*\n'
    )
    if auction.offers_number:
        response_message += (
            f'✅ Количество тендеров в аукционе: *{auction.offers_number}*\n'
        )
    else:
        response_message += (
            f'❌ *Тендеры не найдены*\n'
        )
    response_message += (
        f'⏱ Последнее обновление: *{last_updated.strftime("%d.%m.%Y")}*\n\n'
        f'➡️ {auction_link}\n'
    )
    return response_message


def receive_parsed_auction_message(auction_list: list[AuctionTable]) -> str:
    response_message = (
        f'🚀*Icetrade_bot*\n\n'
    )
    for index, auction in enumerate(auction_list, start=1):
        auction_link = link(f'Ссылка на аукцион', f'{auction.link}')
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


def receive_not_found_auction_message(auction_link: str) -> str:
    auction_link = link(f'Ссылка на аукцион', f'{auction_link}')
    response_message = (
        f'🚀*Icetrade_bot*\n\n'
        f'❌ *Тендеры не найдены*\n\n'
        f'➡️ {auction_link}\n'
    )
    return response_message
