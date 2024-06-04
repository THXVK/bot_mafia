from dotenv import load_dotenv
from os import getenv

DB_NAME = 'sqlite3.db'
load_dotenv()
TOKEN = getenv('TOKEN')

