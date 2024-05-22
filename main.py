import asyncio
import logging
from time import sleep

from services.balances import update_balances
from services.google_storage import GoogleStorage
from services.logger import init_logger
from settings.settings import settings


def main():
    init_logger()
    logging.info('Start AIX balance watcher')
    while True:
        try:
            storage = GoogleStorage(settings.spreadsheet_id, settings.sheet_id)
            wallets = storage.get_wallets()
            loop = asyncio.get_event_loop()
            updated_wallets = loop.run_until_complete(update_balances(wallets))
            storage.update_wallets(updated_wallets)
            logging.info(f'Successfully updated... fall asleep for {settings.sleep} seconds \n')
        except BaseException as error:
            logging.exception(f'ERROR: {error}')
        sleep(settings.sleep)


if __name__ == '__main__':
    main()
