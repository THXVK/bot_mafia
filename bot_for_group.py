from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from bot import change_settings, message_counter
from data import add_new_user, is_user_in_table, get_session_data, is_session_in_table, get_user_data, update_user_data, \
    get_table_data

from keyboards import settings_markup
router = Router()


@router.message(Command('start_game'))
async def start_game(message):
    if message.chat.id < 0:  # id сообщений групповых чатов меньше нуля
        if await is_user_in_table(message.from_user.id):
            if not await is_session_in_table(message.chat.id):
                await message.answer('чтобы присоединиться к игре начните диалог с ботом и дождитесь начала игры')  # todo: поменять текст
                await change_settings(message)
            else:
                await message.reply('в группе уже есть начатая игра')
        else:
            await message.reply('для начала напишите мне в лс')
    else:
        await message.answer('это команда для групповых чатов!')


@router.message(Command('join'))
async def join_register(message: Message):
    if await is_user_in_table(message.from_user.id):
        group_id = message.chat.id
        data = await get_session_data(group_id)

        if not await is_session_in_table(group_id):  # проверка на наличие игры в этой группе
            await message.reply('в вашем чате еще нет начатых игр')
        elif not data[4]:  # проверка на ход игры
            await message.reply('идет настройка')
        else:
            users_group_id = (await get_user_data(message.from_user.id))[1]
            if users_group_id == group_id:  # проверка на наличие в игре
                await message.reply('вы уже в лобби')
            else:
                data_2 = await get_table_data('group_id', group_id)
                num = len(data_2)
                max_num = data[2]
                if num < max_num:  # проверка на предел игроков
                    await update_user_data(message.from_user.id, 'group_id', group_id)
                    await message.reply('вы приняты!')

                    data_2_upd = await get_table_data('group_id', group_id)
                    num_upd = len(data_2_upd)
                    await message_counter(group_id, num_upd)
                elif num == max_num:
                    await message.answer('**начало игры**')


                    ...


                else:
                    await message.reply('достигнут предел игроков')
    else:
        await message.reply('напиши мне в лс команду "/start"')
