from dotenv import load_dotenv
from os import getenv
import keyboards as kb

DB_NAME = 'sqlite3.db'
load_dotenv()
TOKEN = getenv('TOKEN')
DEFAULT_PLAYERS_NUM = 5
MAX_PLAYERS_NUM = 15
DEFAULT_MAFIAS_NUM = 2
mk_dict = {'k': kb.players_num_markup(DEFAULT_PLAYERS_NUM)}

