from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from config import TOKEN, DEFAULT_PLAYERS_NUM
from data import add_new_user, add_new_session, is_user_in_table, update_row
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
    await update_row(message.from_user.id, 'group_id', s_id)
    await bot.send_message(message.from_user.id, 'выберите нужные настройки', reply_markup=await settings_markup())


@router.callback_query(F.data.startswith('set'))
async def new_menu(call: CallbackQuery):
    await call.message.edit_text('выберите число игроков')
    # todo: данные с бд
    await call.message.edit_reply_markup(reply_markup=await players_num_markup(DEFAULT_PLAYERS_NUM))


@router.callback_query(F.data.startswith('pn'))
async def change_players_num(call: CallbackQuery):
    marker, action, num = call.data.split('_')
    if action == 'minus':
        print()
    else:
        ...


@router.callback_query(F.data == 'get-back')
async def change_players_num(call: CallbackQuery):
    await call.message.edit_text('выберите нужные настройки')
    await call.message.edit_reply_markup(reply_markup=await settings_markup())
