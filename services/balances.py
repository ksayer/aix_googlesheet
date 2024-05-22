import asyncio
import json
import logging

from web3 import Web3, AsyncWeb3
from web3.contract import AsyncContract

from services.utils import list_chunks
from services.wallets import Wallet
from settings.settings import settings


async def fetch_balance(wallet: Wallet, contract: AsyncContract, w3: AsyncWeb3, decimals: int):
    try:
        balance = await contract.functions.balanceOf(w3.to_checksum_address(wallet.address)).call()
        wallet.live_balance_wei = balance
        wallet.live_balance = balance / 10 ** decimals
        logging.info(f'Wallet: {wallet.address} balance: {wallet.live_balance}')
    except BaseException as error:
        logging.info(f'Failed while fetching balance: {error}')


async def update_balances(wallets: list[Wallet]) -> list[Wallet]:
    w3 = AsyncWeb3(Web3.AsyncHTTPProvider(settings.eth_rpc))
    with open('settings/erc20abi.json', 'r') as abi:
        contract = w3.eth.contract(address=w3.to_checksum_address(settings.contract_address), abi=json.load(abi))
    decimals = await contract.functions.decimals().call()
    for wallet_chunk in list_chunks(wallets, size=8):
        tasks = [fetch_balance(wallet, contract, w3, decimals) for wallet in wallet_chunk]
        await asyncio.gather(*tasks)
        await asyncio.sleep(1)

    return wallets
