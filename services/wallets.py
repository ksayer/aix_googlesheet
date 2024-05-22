from dataclasses import dataclass


@dataclass
class Wallet:
    address: str
    row: int
    table_balance: float
    live_balance_wei: int | None = None
    live_balance: float | None = None
