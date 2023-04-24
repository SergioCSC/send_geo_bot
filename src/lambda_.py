import config as cfg
import google_sheets
import location_parser

from aiogram import Bot, Dispatcher, types
from aiogram import F

import json
import logging
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import requests


TELEGRAM_BOT_API_PREFIX = 'https://api.telegram.org/bot'

dp = Dispatcher()
bot = Bot(cfg.TELEGRAM_BOT_TOKEN, parse_mode="HTML")


def save_location(location_message: types.Message) -> None:
    id, name, firstname, time, point = location_parser.parse(location_message)
    name = '@' + name
    # time = time.astimezone(ZoneInfo())
    time = time + timedelta(hours=cfg.TIMEDELTA)
    time_str = time.strftime('%H:%M:%S')
    google_sheets.post(id, name, firstname, time_str, point.latitude, point.longitude)
    pass


@dp.edited_message(F.location)
async def any_edited_message(message: types.Message, bot: Bot) -> any:
    # await message.answer('ещё гео')
    save_location(message)


@dp.message(F.location)
async def any_message(message: types.Message) -> any:
    await message.answer('Поймал ваше гео')
    save_location(message)


def lambda_f(event: dict, context) -> None:
    update = event['body']
    logging.debug('update: ' + str(update))
    update = json.loads(update)
    asyncio.get_event_loop().run_until_complete(dp.feed_raw_update(bot, update))
    logging.debug('Return from asyncio loop and from Lambda')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def set_webhook() -> None:
    set_webhook_url = f'{TELEGRAM_BOT_API_PREFIX}{cfg.TELEGRAM_BOT_TOKEN}' \
        f'/setwebhook?url={cfg.AWS_LAMBDA_API_GATEWAY_URL}' \
        f'&max_connections=20'
    logging.debug(f'{set_webhook_url = }')
    requests.get(set_webhook_url)


def delete_webhook() -> None:

    delete_webhook_url = f'{TELEGRAM_BOT_API_PREFIX}{cfg.TELEGRAM_BOT_TOKEN}' \
        '/deletewebhook'
    requests.get(delete_webhook_url)


async def main() -> None:
    delete_webhook()
    await dp.start_polling(bot)
    set_webhook()


if __name__ == '__main__':
    # asyncio.run(main())
    
    event_path = Path('samples','lambda_events', 'share_location_continue.json')
    with open(event_path) as f:
        event = json.load(f)
    lambda_f(event, None)
