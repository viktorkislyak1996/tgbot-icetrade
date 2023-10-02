from aiogram.utils.markdown import link


def receive_article_message(article: int, card_data: dict) -> str:
    article_link = link(f'{article}', f'https://www.wildberries.ru/catalog/{article}/detail.aspx')
    response_message = (
        f'🔎*MP-Control*\n\n'
        f'• Артикул: {article_link}\n'
        f'• Наименование: *{card_data["name"]}*\n'
        f'• Бренд: *{card_data["brand"]}*\n'
        f'• Цена без скидки: *{card_data["price_without_discount"]} руб.*\n'
        f'• Цена со скидкой: *{card_data["price_with_discount"]} руб.*\n'
        f'• Скидка: *{card_data["discount"]} %*\n'
        f'• Остаток: *{card_data["remains"]} шт.*\n\n'
    )
    if card_data['is_spp']:
        response_message += (
            f'✅ *СПП применяется*\n'
            f'🔥Скидка WB для клиента(СПП): *{card_data["spp"]} %*\n'
            f'🔥Цена для клиента: *{card_data["price_for_users"]} руб.*\n\n'
            f'_* Указана максимальная скидка для клиента_\n'
        )
    else:
        response_message += (
            f'❌ *СПП не применяется*\n'
            f'🔥Цена для клиента: *{card_data["price_for_users"]} руб.*\n'
        )
    extension_link = link(
        'Скачай бесплатное расширение',
        'https://chrome.google.com/webstore/detail/mp-control-автоматизация/'
        'dbphhhkgidjeafdabammodmofgglibkb?hl=ru&authuser=0'
    )
    response_message += (
        f'—————————————\n'
        f'MP-Control - управляй рекламой - получай больше прибыли. {extension_link}'
    )
    return response_message
