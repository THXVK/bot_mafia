from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def settings_markup():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='пенис')]
    ]
    )

    return markup
