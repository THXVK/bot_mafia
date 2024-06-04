import sqlite3
from config import DB_NAME
from log import logger


# region python_data
# endregion


def create_db():
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


# region user_db


async def create_users_data_table():
    sql_query = (
        "CREATE TABLE IF NOT EXISTS users_data "
        "(id INTEGER PRIMARY KEY, "
        "session_id INTEGER, "
        "user_id INTEGER, "
        "alive INTEGER, "
        "role TEXT);"
    )
    await execute_query('create_users_data_table', sql_query)


async def add_new_user(session_id: int, user_id: int) -> bool:
    if not is_user_in_table(user_id):
        sql_query = (
            "INSERT INTO users_data "
            "(session_id, user_id, alive, role) "
            "VALUES (?, ?, 0, guest);"
        )

        await execute_query('add_new_user', sql_query, (session_id, user_id))
        return True
    else:
        return False


async def is_user_in_table(user_id: int) -> bool:
    sql_query = (
        'SELECT * '
        'FROM users_data '
        'WHERE user_id = ?;'
    )
    return bool(execute_query('is_user_in_table', sql_query, (user_id,)))


async def get_user_data(user_id: int):
    if is_user_in_table(user_id):
        sql_query = (
            f'SELECT * '
            f'FROM users_data '
            f'WHERE user_id = {user_id};'
        )
        row = await execute_query('get_user_data', sql_query)
        return row


async def update_row(user_id: int, column_name: str, new_value: str | int | None) -> bool:
    if is_user_in_table(user_id):
        sql_query = (
            f"UPDATE users_data "
            f"SET {column_name} = ? "
            f"WHERE user_id = ?;"
        )

        await execute_query('update_row', sql_query, (new_value, user_id))
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

create_db()
create_users_data_table()
