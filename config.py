from dotenv import load_dotenv
from os import getenv

DB_NAME = 'sqlite3.db'
load_dotenv()
TOKEN = getenv('TOKEN')
DEFAULT_PLAYERS_NUM = 5
MAX_PLAYERS_NUM = 15
DEFAULT_MAFIAS_NUM = 2
ROLES_LIST = ['role 1', 'role 2', 'role 3', 'role 4', 'role 5',]
FULL_ROLES_LIST = ['житель', 'мафия', 'шериф', 'лунатик', 'джокер',]

