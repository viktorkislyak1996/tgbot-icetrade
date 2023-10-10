from aiogram import Bot
from aiogram.enums import ParseMode
from sqlalchemy.orm import sessionmaker

from bot.utils import get_auctions_diff
from db import get_all_tracking_auctions, update_auction, get_user_by_id
from bot.keyboards import get_inline_run_tracking_keyboard
from bot.scraper import IcetradeScraper
from bot.messages import receive_parsed_scheduler_message


async def auction_tracker(bot: Bot, session: sessionmaker) -> None:
    """
    The periodic task that tracks Icetrade auction changes
    and sends a telegram message with info about new tenders

    Args:
        bot: The telegram bot
        session: The SQLAlchemy async session
    """
    tracking_auctions = await get_all_tracking_auctions(session)
    user_id = None
    user_telegram_id = None
    for auction in tracking_auctions:
        keyboard = get_inline_run_tracking_keyboard(auction.keyword)

        parser = IcetradeScraper(auction.keyword)
        auction_list = await parser.get_auction()
        if not auction_list:
            continue

        old_number = auction.number
        if not old_number:
            new_auction_list = auction_list
        else:
            new_auction_list = get_auctions_diff(auction_list, old_number)
        if not new_auction_list:
            continue

        auction_info = await parser.get_auction_info(auction_list)
        update_auction_data = {
            'offers_number': auction_info['offers_number'],
            'number': auction_info['last_tender'].number
        }
        await update_auction(auction, update_auction_data, session)

        if auction.user_id != user_id:
            user = await get_user_by_id(auction.user_id, session)
            user_telegram_id = user.telegram_id

        response_message = receive_parsed_scheduler_message(new_auction_list, auction.keyword)
        await bot.send_message(
            user_telegram_id,
            response_message,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
