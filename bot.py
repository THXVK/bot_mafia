from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from config import TOKEN, DEFAULT_PLAYERS_NUM, MAX_PLAYERS_NUM
from data import add_new_user, add_new_session, is_user_in_table, update_user_data, get_user_data, get_session_data, \
    update_session_data
from keyboards import settings_markup, players_num_markup

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
    await call.message.edit_text('выберите число игроков')
    # todo: данные с бд
    await call.message.edit_reply_markup(reply_markup=await players_num_markup(DEFAULT_PLAYERS_NUM))


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
