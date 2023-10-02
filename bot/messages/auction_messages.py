from aiogram.utils.markdown import link

from db import Auction


def receive_product_message(auction: Auction) -> str:
    auction_link = link(f'Ссылка на аукцион', f'{auction.link}')
    response_message = (
        f'🔎*Icetrade_bot*\n\n'
        f'• Краткое описание: *{auction.description}*\n'
        f'• Наименование заказчика: *{auction.customer_name}*\n'
        f'• Страна: *{auction.country}*\n'
        f'• Номер: *{auction.number}*\n'
        f'• Стоимость: *{auction.price} {auction.currency}*\n'
        f'• Действует до: *{auction.expires_at}*\n\n'
        f'• {auction_link}\n\n'
    )
    return response_message
