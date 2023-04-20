import sys
from os import environ

IN_LINUX = sys.platform == 'linux'

TELEGRAM_BOT_TOKEN = environ['TELEGRAM_BOT_TOKEN']
GOOGLE_SPREADSHEET_ID = environ['GOOGLE_SPREADSHEET_ID']

TIMEDELTA = 4  # Georgia timezone is GMT+04