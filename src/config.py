import sys
from os import environ
import logging

IN_AWS_LAMBDA = 'AWS_LAMBDA_RUNTIME_API' in environ

TELEGRAM_BOT_TOKEN = environ['TELEGRAM_BOT_TOKEN']
GOOGLE_SPREADSHEET_ID = environ['GOOGLE_SPREADSHEET_ID']

TIMEDELTA = 4  # Georgia timezone is GMT+04

# if you want to set webhook
AWS_LAMBDA_API_GATEWAY_URL=environ.get('AWS_LAMBDA_API_GATEWAY_URL')

# Configure logging
log_level = environ.get('LOG_LEVEL', 'INFO')
logging.getLogger().setLevel(log_level)  # for aws lambda
