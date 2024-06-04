from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from bot import change_settings
from data import add_new_user, is_user_in_table

from keyboards import settings_markup
router = Router()


@router.message(Command('start_game'))
async def start_game(message):
    if is_user_in_table(message.chat.id):
        await message.answer('чтобы присоединиться к игре начните диалог с ботом')
        await change_settings(message)
    else:
        await message.reply('для начала напишите мне в лс')




@router.message(Command('join'))
async def join_register(message: Message):
    if is_user_in_table(message.from_user.id):
        if ...:
            ...
        elif ...:
            ...
        else:
            ...
            await message.reply('вы приняты!')
    else:
        await message.reply('напиши мне в лс команду "/start"')
