from aiogram.utils.markdown import link

from bot.parser import AuctionTable
from db import Auction


def receive_auction_message(auction_list: list[AuctionTable]) -> str:
    response_message = (
        f'🚀*Icetrade_bot*\n\n'
    )
    for auction in auction_list:
        auction_link = link(f'Ссылка на аукцион', f'{auction.link}')
        response_message += (
            f'🔹 Краткое описание: *{auction.description}*\n'
            f'🔹 Наименование заказчика: *{auction.customer_name}*\n'
            f'🔹 Номер: *{auction.number}*\n'
            f'🌎 Страна: *{auction.country}*\n'
            f'💰 Стоимость: *{auction.cost}*\n'
            f'⏳ Действует до: *{auction.expires_at}*\n\n'
            f'➡️ {auction_link}\n'
            f'————————————————————————\n\n'
        )
    return response_message


# def receive_auction_message(auction: Auction) -> str:
#     auction_link = link(f'Ссылка на аукцион', f'{auction.link}')
#     response_message = (
#         f'🔎*Icetrade_bot*\n\n'
#         f'• Краткое описание: *{auction.description}*\n'
#         f'• Наименование заказчика: *{auction.customer_name}*\n'
#         f'• Страна: *{auction.country}*\n'
#         f'• Номер: *{auction.number}*\n'
#         f'• Стоимость: *{auction.price} {auction.currency}*\n'
#         f'• Действует до: *{auction.expires_at}*\n\n'
#         f'• {auction_link}\n\n'
#     )
#     return response_message