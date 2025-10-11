from src.main.api.models.base_model import BM
from typing import List
from datetime import datetime


class DepositMoneyResponse(BM):
    id: int
    accountNumber: str
    balance: float
    transactions: List[dict[str, int | float | str | datetime]]