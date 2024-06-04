from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from data import add_new_user

router = Router()


@router.message(CommandStart())
async def start_message(message: Message):
    if res := await add_new_user(0, message.from_user.id)
        await message.answer('добро пожаловать!')
    else:
        await message.answer('вы уже в базе')



# @router.message(Command('join'))
# async def join_register(message: Message):
#     if is_user_in_table():
#         if ...:
#             ...
#         elif ...:
#             ...
#         else:
#             ...
#             await message.reply('вы приняты!')
#     else:
#         await message.reply('напиши мне в лс команду "/start"')
#


