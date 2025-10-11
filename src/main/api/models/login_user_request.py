from src.main.api.models.base_model import BM

class LoginUserRequest(BM):
    username: str
    password: str