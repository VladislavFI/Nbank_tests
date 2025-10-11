from pydantic import BaseModel as BM


class TransferMoneyRequest(BM):
    senderAccountId: int
    receiverAccountId: int
    amount: int
