from __future__ import print_function

import config as cfg

from aiogram.types.location import Location

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path
import logging
from datetime import datetime


# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def _get_credentials() -> Credentials:
    logging.debug(f'{_get_credentials.__name__} START')
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google_key.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        if cfg.IN_LINUX:  # can't save to disk in aws lambda
            # logging.debug(f'{creds.to_json() = }')
            pass
        else:
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    
    logging.debug(f'{_get_credentials.__name__} STOP')
    return creds


def post(user_id: int, name: str, firstname: str, time: datetime, lat: str, lon: str) -> None:
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    
    creds: Credentials = _get_credentials()
    
    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        
        body = {
            'values': [
                [
                    user_id, name, firstname, str(time), lat, lon, 'локация'
                ],
            ],
        }
        range = f'Sheet1!A1:Z'
        result = sheet.values().append(
            spreadsheetId=cfg.GOOGLE_SPREADSHEET_ID,
            range=range,
            insertDataOption="INSERT_ROWS",
            valueInputOption='USER_ENTERED',
            body=body,
        ).execute()
        logging.info(f"updatedRange: {result.get('updates').get('updatedRange')}")
        return result

    except HttpError as err:
        logging.info(err)
