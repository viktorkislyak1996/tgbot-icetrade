from aiogram.utils.markdown import link


def receive_scheduler_message(
        card_data: dict,
        new_price: float | None,
        new_spp: int | None,
        old_price: float | None,
        old_spp: int | None
) -> str:
    article_link = link(f'{card_data["wb_id"]}', f'https://www.wildberries.ru/catalog/{card_data["wb_id"]}/detail.aspx')
    response_message = (
        f'🔎*MP-Control*\n\n'
    )

    if new_spp and old_spp:
        if new_spp > old_spp:
            spp_diff = new_spp - old_spp
            response_message += (
                f'⬆️СПП УВЕЛИЧИЛОСЬ НА *{spp_diff} %*\n'
                f'Предыдущее значение: *{old_spp} %*\n'
                f'Новое значение: *{new_spp} %*\n\n'
            )
        elif old_spp > new_spp:
            spp_diff = old_spp - new_spp
            response_message += (
                f'⬇️СПП УМЕНЬШИЛОСЬ НА *{spp_diff} %*\n'
                f'Предыдущее значение: *{old_spp} %*\n'
                f'Новое значение: *{new_spp} %*\n\n'
            )

    if new_price and old_price:
        if new_price > old_price:
            price_diff = new_price - old_price
            response_message += (
                f'⬆️ЦЕНА УВЕЛИЧИЛАСЬ НА *{price_diff} руб.*\n'
                f'Предыдущее значение: *{old_price} руб.*\n'
                f'Новое значение: *{new_price} руб.*\n\n'
            )
        elif old_price > new_price:
            price_diff = old_price - new_price
            response_message += (
                f'⬇️ЦЕНА УМЕНЬШИЛАСЬ НА *{price_diff} руб.*\n'
                f'Предыдущее значение: *{old_price} руб.*\n'
                f'Новое значение: *{new_price} руб.*\n\n'
            )

    if new_spp and not old_spp:
        response_message += (
            f'✅У ВАС ПОЯВИЛОСЬ СПП!\n'
            f'Предыдущее значение: *0 %*\n'
            f'Новое значение: *{new_spp} %*\n\n'
        )
    elif old_spp and not new_spp:
        response_message += (
            f'❗️У ВАС ПРОПАЛО СПП!\n'
            f'Предыдущее значение: *{old_spp} %*\n'
            f'Новое значение: *0 %*\n\n'
        )

    response_message += (
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
