from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.methods import send_message
from aiogram.types import Message

from config import TOKEN
from data import add_new_user
from keyboards import settings_markup

bot = Bot(TOKEN)
router = Router()


@router.message(CommandStart())
async def start_message(message: Message):
    if res := await add_new_user(0, message.from_user.id):
        await message.answer('добро пожаловать!')
    else:
        await message.answer('вы уже в базе')


@router.message(Command('change_settings'))
async def change_settings(message: Message):
    await bot.send_message(message.from_user.id, 'выберите нужные настройки', reply_markup=await settings_markup())

