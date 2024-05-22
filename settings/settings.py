from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    spreadsheet_id: str
    sheet_id: int
    contract_address: str
    sleep: int = 10 * 60
    eth_rpc: str


settings: Settings = Settings()
