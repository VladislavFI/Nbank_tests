from src.main.api.models.base_model import BM


class TransferMoneyResponse(BM):
    message: str
    amount: float
    receiverAccountId: int
    senderAccountId: int
