from typing import List
from src.main.api.models.base_model import BM



class LoginUserResponse(BM):
    role: str
    username: str