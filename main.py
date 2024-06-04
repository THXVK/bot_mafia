import asyncio
from log import logger

from aiogram import Bot, Dispatcher
from config import TOKEN
from bot import router as router_1
from bot_for_group import router as router_2

bot = Bot(TOKEN)
dp = Dispatcher()


async def main():
    dp.include_routers(router_1, router_2)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
