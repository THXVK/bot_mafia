from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from data import add_new_user

router = Router()


@router.message(Command('start_game'))
async def start_game(message):
    ...
