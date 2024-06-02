import sqlite3
from config import
from log import logger


# region python_data
# endregion


# region sql
def create_db():
    connection = sqlite3.connect('sqlite3.db')
    connection.close()


def execute_query(func_name: str, query: str, data: tuple | None = None, db_name: str = DB_NAME):
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


def create_users_data_table():
    sql_query = (
        "CREATE TABLE IF NOT EXISTS users_data "
        "(session_id INTEGER PRIMARY KEY, "
        "session_id INTEGER, "
        "user_id INTEGER, "
        "alive INTEGER, "
        "role TEXT);"
    )
    execute_query('create_users_data_table', sql_query)


def add_new_user(user_id: int) -> bool:
    if not is_user_in_table(user_id):
        sql_query = (
            "INSERT INTO users_data "
            "(user_id, gpt_tokens, stt_blocks, tts_simbols, dialogue_story) "
            "VALUES (?, ?, ?, ?, ?);"
        )

        execute_query('add_new_user', sql_query, (user_id, MAX_TOKENS_PER_USER, MAX_STT_BLOCKS_PER_USER, TTS_SIMBOLS_PER_USER, ''))
        return True
    else:
        return False


def is_user_in_table(user_id: int) -> bool:
    sql_query = (
        'SELECT * '
        'FROM users_data '
        'WHERE user_id = ?;'
    )
    return bool(execute_query('is_user_in_table', sql_query, (user_id,)))


def get_user_data(user_id: int):
    if is_user_in_table(user_id):
        sql_query = (
            f'SELECT * '
            f'FROM users_data '
            f'WHERE user_id = {user_id};'
        )
        row = execute_query('get_user_data', sql_query)[0]
        return row


def update_row(user_id: int, column_name: str, new_value: str | int | None) -> bool:
    if is_user_in_table(user_id):
        sql_query = (
            f"UPDATE users_data "
            f"SET {column_name} = ? "
            f"WHERE user_id = ?;"
        )

        execute_query('update_row', sql_query, (new_value, user_id))
        return True
    else:
        return False


def get_table_data():
    sql_query = (
        f'SELECT * '
        f'FROM users_data;'
    )
    res = execute_query('get_table_data', sql_query)
    if not res:
        res = []
    return res




create_db()
create_users_data_table()