import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import TOKEN

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message()
async def start_message(message: Message):
    await message.answer('привет! ')


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
