from typing import List
from src.main.api.models.base_model import BM


class Transaction(BM):
    id: int
    amount: float
    type: str
    timestamp: str
    relatedAccountId: int


class Account(BM):
    id: int
    accountNumber: str
    balance: float
    transactions: List[Transaction]


class Customer(BM):
    id: int
    username: str
    password: str
    name: str
    role: str
    accounts: List[Account]


class ChangeNameUserResponse(BM):
    message: str
    customer: Customer