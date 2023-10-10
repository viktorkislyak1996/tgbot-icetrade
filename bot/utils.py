import re

from aiogram import types
from aiogram.types import CallbackQuery
from sqlalchemy.orm import sessionmaker

from bot.scraper import AuctionTable
from db import get_user_by_telegram_id, create_user, User

digit_to_emoji = {
    1: '1️⃣',
    2: '2️⃣',
    3: '3️⃣',
    4: '4️⃣',
    5: '5️⃣'
}


async def receive_user_from_message(message: types.Message | CallbackQuery, session: sessionmaker) -> User:
    user_telegram_id = int(message.from_user.id)
    user_data = {
        'name': message.from_user.username,
        'telegram_id': user_telegram_id
    }
    user = await get_user_by_telegram_id(user_telegram_id, session)
    if not user:
        user = await create_user(user_data, session)
    return user


def receive_keyword_from_message(message: types.Message) -> str:
    keyword = " ".join(re.findall("[а-яА-ЯёЁ]+", message.text))
    return keyword


def receive_keyword_from_callback(callback: CallbackQuery) -> str:
    keyword = callback.data.split('_')[-1]
    return keyword


def is_first_number_greater(num1: str, num2: str) -> bool:
    num1_split = num1.split('-')
    num2_split = num2.split('-')
    num1_year, num1_number = int(num1_split[0]), int(num1_split[1])
    num2_year, num2_number = int(num2_split[0]), int(num2_split[1])
    if num1_year > num2_year:
        return True
    elif num1_year == num2_year:
        if num1_number > num2_number:
            return True
        else:
            return False
    else:
        return False


def get_auctions_diff(auction_list: list[AuctionTable], old_number: str) -> list[AuctionTable]:
    result = []
    for auction in auction_list:
        if is_first_number_greater(auction.number, old_number):
            result.append(auction)
    return result
