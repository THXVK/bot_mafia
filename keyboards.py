from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import ROLES_LIST


async def settings_markup():
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='число игроков', callback_data='set_players-num'),
         InlineKeyboardButton(text='исключенные роли', callback_data='set_banned-roles')],

        [InlineKeyboardButton(text='сбросить', callback_data='set_roll-back'),
         InlineKeyboardButton(text='начать игру', callback_data='set_start-the-game')]
    ])

    return markup


async def players_num_markup(current_num: int):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='-', callback_data=f'pn_minus'),
            InlineKeyboardButton(text=f'{current_num}', callback_data='null'),
            InlineKeyboardButton(text='+', callback_data=f'pn_plus')],
        [InlineKeyboardButton(text='<-', callback_data='get-back')]
    ])
    return markup  # если число игроков - 13, то появляется секретная роль - джокер


async def gen_roles_markup(banned_roles_list: list | None = []):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='! ' + role if role in banned_roles_list else '? ' + role,
                              callback_data=f'ban_{role}') for role in ROLES_LIST[0:3]],
        [InlineKeyboardButton(text='! ' + role if role in banned_roles_list else '? ' + role,
                              callback_data=f'ban_{role}') for role in ROLES_LIST[3:5]],
        [InlineKeyboardButton(text='<-', callback_data='get-back')]
    ])
    return markup


async def gen_vote_markup(players_list):
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f'{name}', callback_data=f'vote-for_{name}')] for name in players_list
    ])

    return markup


async def gen_vics_markup():
    ...

