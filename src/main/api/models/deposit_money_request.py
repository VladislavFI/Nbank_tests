from src.main.api.models.base_model import BM

class DepositMoneyRequest(BM):
    id: int
    balance: int