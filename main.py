import asyncio
import logging
from threading import Thread
from time import sleep
from api import start_api_server
from services.balances import update_balances
from services.google_storage import GoogleStorage
from services.logger import init_logger
from settings.settings import settings


async def balance_watcher():
    init_logger()
    logging.info('Start AGIX balance watcher')
    while True:
        try:
            storage = GoogleStorage(settings.spreadsheet_id, settings.sheet_id)
            wallets = storage.get_wallets()
            await update_balances(wallets)
            storage.update_wallets(wallets)
            logging.info(f'Successfully updated... fall asleep for {settings.sleep} seconds \n')
        except BaseException as error:
            logging.exception(f'ERROR: {error}')
        sleep(settings.sleep)


if __name__ == '__main__':
    asyncio.run(balance_watcher())
