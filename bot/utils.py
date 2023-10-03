import re

from aiogram import types
from aiogram.types import CallbackQuery
from sqlalchemy.orm import sessionmaker

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
