from src.main.api.models.base_model import BaseModel
from typing import List, Optional
from datetime import datetime


class Transaction(BaseModel):
    id: int
    amount: float
    type: str
    timestamp: datetime
    relatedAccountId: int


class Account(BaseModel):
    id: int
    accountNumber: str
    balance: float
    transactions: List[Transaction]


class CustomerProfileResponse(BaseModel):
    id: int
    username: str
    password: str
    name: Optional[str]
    role: str
    accounts: List[Account]