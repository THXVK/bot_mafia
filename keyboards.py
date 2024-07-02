from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def settings_markup():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='число игроков', callback_data='set_players-num'),
         InlineKeyboardButton(text='исключенные роли', callback_data='set_banned-roles')],

        [InlineKeyboardButton(text='сбросить', callback_data='set_roll-back'),
         InlineKeyboardButton(text='начать игру', callback_data='set_start-the-game')]
    ])

    return markup


async def players_num_markup(current_num):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'установлено: {current_num}', callback_data='null')],
        [InlineKeyboardButton(text='-', callback_data=f'pn_minus'),
            InlineKeyboardButton(text='+', callback_data=f'pn_plus')],
        [InlineKeyboardButton(text='<-', callback_data='get-back')]
    ])
    return markup  # если число игроков - 13, то появляется секретная роль - джокер



