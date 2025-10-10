from src.main.api.models.base_model import BM

class CreateUserRequest(BM):
    username: str
    password: str
    role: str