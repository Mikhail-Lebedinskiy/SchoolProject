from pprint import pprint

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


def read_google_sheets(s):
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=s,
        majorDimension='ROWS'
    ).execute()
    return values['values'][0]


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'Project-99f7721baf37.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1walrfWQ65rxYF7dArX1HNOYYx9ROMo18jnK9NP2CRn0'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

pprint(read_google_sheets('A1:A1'))
