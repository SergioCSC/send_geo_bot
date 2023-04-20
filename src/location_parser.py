from datetime import datetime

from aiogram import types
from aiogram.types.location import Location


def parse(message: types.Message) -> tuple[int, str, str, datetime, Location]:
    id = message.from_user.id
    name = message.from_user.username
    firstname = message.from_user.first_name
    date = datetime.fromtimestamp(message.edit_date) if message.edit_date else message.date
    location = message.location
    return id, name, firstname, date, location