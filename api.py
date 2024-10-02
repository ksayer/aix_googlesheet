import logging

import redis
from fastapi import FastAPI
import uvicorn

from services.balances import check_balance
from settings.settings import settings

app = FastAPI()
start_balance = 100_000_000

redis_client = redis.StrictRedis(host=settings.redis_host, port=settings.redis_port, db=0)


@app.get("/info/api/total_supply")
async def get_total_supply():
    try:
        cached_balance = redis_client.get("dead_balance")
        if cached_balance:
            dead_balance = int(cached_balance)
            logging.info(f"Returning cached balance: {dead_balance}")
        else:
            dead_balance = await check_balance('0x000000000000000000000000000000000000dEaD')
            redis_client.set("dead_balance", dead_balance, ex=300)
            logging.info(f"Balance cached: {dead_balance}")

        total_supply = start_balance - dead_balance / 10 ** 18
        logging.info(f"Total supply {total_supply=}")
        return total_supply
    except BaseException as error:
        logging.exception(f"Error total supply {error=}")
        return start_balance


@app.get("/info/api/circulating_supply")
async def get_circulating_supply():
    return start_balance


def start_api_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    start_api_server()