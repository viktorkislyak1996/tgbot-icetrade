from aiogram import types
from aiogram.enums import ParseMode
from sqlalchemy.orm import sessionmaker

from db import get_all_tracking_auctions_by_user_id
from bot.keyboards import get_inline_run_tracking_keyboard
from bot.utils import receive_user_from_message
from bot.messages import receive_auction_message


async def keywords(message: types.Message, session: sessionmaker) -> None:
    user = await receive_user_from_message(message, session)

    tracking_auctions = await get_all_tracking_auctions_by_user_id(user.id, session)
    for auction in tracking_auctions:
        keyboard = get_inline_run_tracking_keyboard(auction.keyword)

        response_message = receive_auction_message(auction)
        await message.answer(
            response_message,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
    if not tracking_auctions:
        pass
    await message.answer(
        'У вас нет отслеживаемых ключевых слов.\n'
        'Для того, чтобы добавить ключевое слово в отслеживаемые, введите сперва ключевое слово, а затем, '
        'в полученном сообщении, нажмите на кнопку *"Запустить отслеживание аукциона"*',
        parse_mode=ParseMode.MARKDOWN
    )
