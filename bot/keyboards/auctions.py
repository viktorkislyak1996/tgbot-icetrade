from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from db import Auction


def get_inline_tracking_keyboard(auction: Auction, keyword: str) -> InlineKeyboardMarkup:
    buttons = []
    if auction:
        if auction.tracking:
            buttons.append(
                [InlineKeyboardButton(text="Прекратить отслеживание аукциона", callback_data=f'stop_tracking_{keyword}')]
            )
        else:
            buttons.append(
                [InlineKeyboardButton(text="Запустить отслеживание аукциона", callback_data=f'run_tracking_{keyword}')]
            )
    else:
        buttons.append(
            [InlineKeyboardButton(text="Запустить отслеживание аукциона", callback_data=f'run_tracking_{keyword}')])

    buttons.append([InlineKeyboardButton(text="Обновить", callback_data=f'refresh_{keyword}')])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_inline_run_tracking_keyboard(keyword: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Прекратить отслеживание аукциона", callback_data=f'stop_tracking_{keyword}')
        ],
        [
            InlineKeyboardButton(text="Обновить", callback_data=f'refresh_{keyword}')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_inline_stop_tracking_keyboard(keyword: str) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Запустить отслеживание аукциона", callback_data=f'run_tracking_{keyword}'),
        ],
        [
            InlineKeyboardButton(text="Обновить", callback_data=f'refresh_{keyword}')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_reply_tracking_keywords_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="Отслеживаемые ключевые слова")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard
