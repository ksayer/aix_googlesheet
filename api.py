import logging

from fastapi import FastAPI
import uvicorn

from services.balances import check_balance

app = FastAPI()
start_balance = 100_000_000

@app.get("/info/api/total_supply")
async def get_total_supply():
    try:
        if dead_balance := await check_balance('0x000000000000000000000000000000000000dEaD'):
            total_supply =  start_balance - dead_balance / 10 ** 18
            logging.info(f'Total supply {total_supply=}')
            return total_supply
    except BaseException as error:
        logging.exception(f'Error total supply {error=}')
        ...
    logging.info(f'Total supply {start_balance=}')
    return start_balance


@app.get("/info/api/circulating_supply")
async def get_circulating_supply():
    logging.info('Circulating supply')
    return start_balance


def start_api_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)
