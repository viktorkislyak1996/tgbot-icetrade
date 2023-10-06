from aiogram import types
from aiogram.enums import ParseMode


async def help(message: types.Message) -> None:
    await message.answer(
        'Для того, чтобы получить информацию о закупках, '
        'введите ключевое слово, по которому будет осуществляться поиск.\n'
        'Пример: *АСКУЭ*\n'
        '*Внимание*: Длина ключевого слова не должна превышать *25* символов!\n'
        'Если вы хотите отслеживать появление новых закупок, '
        'нажмите на кнопку *"Запустить отслеживание"* в полученном сообщении.\n'
        '*Внимание*: Выводится информация о *5* самых свежих тендерах!\n'
        'Если вы хотите прекратить отслеживание тендеров по ключевому слову, '
        'нажмите на кнопку *"Прекратить отслеживание"*.\n'
        '*Внимание*: Максимальное число отслеживаемых ключевых слов - *20*!\n'
        'Чтобы просмотреть все ключевые слова, которые вы отслеживаете, '
        'выберите в меню пункт *"Отслеживаемые ключевые слова"* или отправьте команду /keywords.',
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )
