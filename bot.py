from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from config import TOKEN, DEFAULT_PLAYERS_NUM, MAX_PLAYERS_NUM, DEFAULT_MAFIAS_NUM
from data import add_new_user, add_new_session, is_user_in_table, update_user_data, get_user_data, get_session_data, \
    update_session_data
from keyboards import settings_markup, players_num_markup, gen_roles_markup

bot = Bot(TOKEN)
router = Router()


@router.message(CommandStart())
async def start_message(message: Message):
    if not await is_user_in_table(message.chat.id):
        await add_new_user(-1, message.from_user.id)
        await message.answer('добро пожаловать!')
        await message.answer('чтобы начать игру добавьте меня в группу и сделайте админом, '
                             'напишите /start_game и игра начнется')
    else:
        await message.answer('вы уже в базе')


async def change_settings(message: Message):
    s_id = message.chat.id
    await add_new_session(s_id)
    await update_user_data(message.from_user.id, 'group_id', s_id)
    await bot.send_message(message.from_user.id, 'выберите нужные настройки', reply_markup=await settings_markup())


@router.callback_query(F.data.startswith('set'))
async def new_menu(call: CallbackQuery):
    data = await get_user_data(call.message.chat.id)
    group_id = data[1]

    if call.data.endswith('players-num'):
        await call.message.edit_text('выберите число игроков')
        await call.message.edit_reply_markup(reply_markup=await players_num_markup(DEFAULT_PLAYERS_NUM))

    elif call.data.endswith('banned-roles'):
        await call.message.edit_text('исключите нужные роли')
        await call.message.edit_reply_markup(reply_markup=await gen_roles_markup())

    elif call.data.endswith('roll-back'):
        await call.message.edit_text('.')
        await update_session_data(group_id, 'players_num', DEFAULT_PLAYERS_NUM)
        await call.message.edit_text('..')
        await update_session_data(group_id, 'mafias_num', DEFAULT_MAFIAS_NUM)
        await call.message.edit_text('...')
        await update_session_data(group_id, 'banned_roles', '')
        await call.message.edit_text('сброшено!')

        await call.message.edit_text('выберите нужные настройки')
        await call.message.edit_reply_markup(reply_markup=await settings_markup())

    else:
        await update_session_data(group_id, 'is_started', 1)
        await bot.send_message(group_id, 'игра началась. Чтобы присоединиться, напишите /join')
        await call.message.edit_text('игра начинается!')  # отслеживание количества игроков


@router.callback_query(F.data.startswith('pn'))
async def change_players_num(call: CallbackQuery):
    marker, action = call.data.split('_')
    data = await get_user_data(call.message.chat.id)
    group_id = data[1]
    data_2 = await get_session_data(group_id)
    cur_num = data_2[2]
    if action == 'minus':
        cur_num -= 1
    else:
        cur_num += 1

    if cur_num < DEFAULT_PLAYERS_NUM:
        cur_num = MAX_PLAYERS_NUM
    elif cur_num > MAX_PLAYERS_NUM:
        cur_num = DEFAULT_PLAYERS_NUM

    await update_session_data(group_id, 'players_num', cur_num)
    await call.message.edit_reply_markup(reply_markup=await players_num_markup(cur_num))


@router.callback_query(F.data == 'get-back')
async def change_players_num(call: CallbackQuery):
    await call.message.edit_text('выберите нужные настройки')
    await call.message.edit_reply_markup(reply_markup=await settings_markup())


@router.callback_query(F.data.startswith('ban'))
async def ban_the_role(call: CallbackQuery):
    role = call.data.split('_')[1]
    data = await get_user_data(call.message.chat.id)
    group_id = data[1]
    data_2 = await get_session_data(group_id)
    banned_roles_str = data_2[5]
    banned_roles_list = banned_roles_str.split(', ')

    if role not in banned_roles_list:
        banned_roles_str += ', ' + role
        banned_roles_list = banned_roles_str.split(', ')
    else:
        banned_roles_list.remove(role)
        banned_roles_str = ', '.join(banned_roles_list)

    await update_session_data(group_id, 'banned_roles', banned_roles_str)
    await call.message.edit_reply_markup(reply_markup=await gen_roles_markup(banned_roles_list))


