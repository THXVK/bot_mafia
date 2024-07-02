import asyncio

from data import create_users_data_table, create_db, create_sessions_data_table
#  from log import logger

from aiogram import Bot, Dispatcher
from config import TOKEN
from bot import router as router_1
from bot_for_group import router as router_2

bot = Bot(TOKEN)
dp = Dispatcher()


async def main():
    await create_db()
    await create_users_data_table()
    await create_sessions_data_table()

    dp.include_routers(router_1, router_2)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
