import logging

from eth_utils import is_address
from google.oauth2 import service_account
from googleapiclient.discovery import build

from services.wallets import Wallet


class GoogleStorage:
    def __init__(self, spreadsheet_id: str, sheet_id: int):
        credentials_file = 'credentials.json'
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.service = build(serviceName='sheets', version='v4', credentials=credentials)
        self.spreadsheet_id = spreadsheet_id
        self.sheet_id = sheet_id

    def get_wallets(self) -> list[Wallet]:
        wallets = []
        for index, row in enumerate(self._get_data()):
            try:
                if row and is_address(address := row[0].strip()):
                    table_balance = float(row[1].replace(',', ''))
                    wallets.append(Wallet(address=address, row=index, table_balance=table_balance))
            except BaseException as error:
                logging.error(f'Get wallet error: {error}')
        return wallets

    def update_wallets(self, wallets: list[Wallet]):
        update_requests = [
            self._prepare_update_dict(row=wallet.row, column=2, value=wallet.live_balance)
            for wallet in wallets if wallet.live_balance and round(wallet.live_balance, 2) != wallet.table_balance
        ]
        logging.info(f'The balance has changed for {len(update_requests)} wallets')
        if update_requests:
            self._update_cells(update_requests)

    def _get_data(self) -> list[list[str]]:
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=f'{self._get_sheet_name()}!B1:C1000'
        ).execute()
        values = result.get('values', [])
        return values

    def _get_sheet_name(self) -> str:
        result = self.service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
        sheet = [s for s in result['sheets'] if s['properties']['sheetId'] == self.sheet_id]
        if not sheet:
            raise ValueError('sheetID not found')
        return sheet[0]['properties']['title']

    def _update_cells(self, requests: list[dict]):
        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={'requests': requests}
        ).execute()

    def _prepare_update_dict(self, row, column, value, data_type='numberValue') -> dict:
        return {
            'updateCells': {
                'rows': [{
                    'values': [{
                        'userEnteredValue': {data_type: value}
                    }]
                }],
                'fields': 'userEnteredValue',
                'start': {
                    'sheetId': self.sheet_id,
                    'rowIndex': row,
                    'columnIndex': column,
                }
            }
        }
