import requests, logging

from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.configs.config import Config


class RequestSpecs:
    @staticmethod
    def default_req_headers():
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    @staticmethod
    def unauth_spec():
        return RequestSpecs.default_req_headers()

    @staticmethod
    def admin_auth_spec():
        headers = RequestSpecs.default_req_headers()
        headers['Authorization'] = Config.get("ADMIN_AUTH_HEADER", "Bacic YWRtaW46cGFzc3dvcmQ=")
        return headers

    @staticmethod
    def user_auth_spec(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url=f'{Config.get('backendUrl')}/auth/login',
            json=request.model_dump()
        )

        if response.status_code == 200:
            headers = RequestSpecs.default_req_headers()
            headers['Authorization'] = response.headers.get('Authorization')
            return headers

        logging.error(f'Authentication failed for {username} with status {response.status_code}')
        raise Exception('Failed to authenticate user')

