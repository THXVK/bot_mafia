import sqlite3
from config import DB_NAME, DEFAULT_MAFIAS_NUM, DEFAULT_PLAYERS_NUM
from log import logger


# region python_data
# endregion


async def create_db():
    connection = sqlite3.connect('sqlite3.db')
    connection.close()


async def execute_query(func_name: str, query: str, data: tuple | None = None, db_name: str = DB_NAME):
    try:
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()

        if data:
            cursor.execute(query, data)
            connection.commit()
        else:
            cursor.execute(query)

    except sqlite3.Error as e:
        error_msg = f"Ошибка в {func_name}: {e}"
        logger.error(error_msg)

    else:
        result = cursor.fetchall()
        connection.close()
        return result

# region sessions_table


async def create_sessions_data_table():
    # только активные игры
    sql_query = (
        "CREATE TABLE IF NOT EXISTS sessions_data "
        "(session_id INTEGER PRIMARY KEY, "
        "group_id INTEGER, "  # уникальное значение (начинается с -)
        "players_num INTEGER, "
        "mafias_num INTEGER, "
        "is_started INTEGER, "
        "banned_roles TEXT);"
    )
    await execute_query('create_users_data_table', sql_query)


async def add_new_session(group_id):
    sql_query = (
        f"INSERT INTO sessions_data "
        f"(group_id, players_num, mafias_num, is_started, banned_roles) "
        f"VALUES (?, {DEFAULT_PLAYERS_NUM}, {DEFAULT_MAFIAS_NUM}, 0, ?);"
    )
    await execute_query('add_new_session', sql_query, (group_id, ''))


async def get_session_data(group_id: int):
    sql_query = (
            f'SELECT * '
            f'FROM sessions_data '
            f'WHERE group_id = {group_id};'
    )
    row = await execute_query('get_session_data', sql_query)
    return row[0]


async def update_session_data(group_id: int, column_name: str, new_value: str | int | None) -> bool:

    sql_query = (
            f"UPDATE sessions_data "
            f"SET {column_name} = ? "
            f"WHERE group_id = ?;"
    )

    await execute_query('update_user_data', sql_query, (new_value, group_id))

# endregion


# region users_table

async def create_users_data_table():
    sql_query = (
        "CREATE TABLE IF NOT EXISTS users_data "
        "(id INTEGER PRIMARY KEY, "
        "group_id INTEGER, "
        "user_id INTEGER, "
        "is_alive INTEGER, "
        "role TEXT, "
        "is_vip INTEGER);"
    )
    await execute_query('create_users_data_table', sql_query)


async def add_new_user(session_id: int, user_id: int) -> bool:
    if not await is_user_in_table(user_id):
        sql_query = (
            "INSERT INTO users_data "
            "(group_id, user_id, is_alive, role, is_vip) "
            "VALUES (?, ?, 0, ?, 0);"
        )

        await execute_query('add_new_user', sql_query, (session_id, user_id, 'guest'))
        return True
    else:
        return False


async def is_user_in_table(user_id: int) -> bool:
    sql_query = (
        'SELECT * '
        'FROM users_data '
        'WHERE user_id = ?;'
    )

    return bool(await execute_query('is_user_in_table', sql_query, (user_id,)))


async def get_user_data(user_id: int):
    if await is_user_in_table(user_id):
        sql_query = (
            f'SELECT * '
            f'FROM users_data '
            f'WHERE user_id = {user_id};'
        )
        row = await execute_query('get_user_data', sql_query)
        return row[0]


async def update_user_data(user_id: int, column_name: str, new_value: str | int | None) -> bool:
    if await is_user_in_table(user_id):
        sql_query = (
            f"UPDATE users_data "
            f"SET {column_name} = ? "
            f"WHERE user_id = ?;"
        )

        await execute_query('update_user_data', sql_query, (new_value, user_id))
        return True
    else:
        return False


async def get_table_data():
    sql_query = (
        f'SELECT * '
        f'FROM users_data;'
    )
    res = await execute_query('get_table_data', sql_query)
    if not res:
        res = []
    return res
# endregion
