import requests
from http import HTTPStatus

from src.main.api.models.customer_profile_response import CustomerProfileResponse
from src.main.api.models.change_name_user_request import ChangeNameUserRequest
from src.main.api.models.change_name_user_response import ChangeNameUserResponse
from src.main.api.requests.requester import Requester


class CustomerProfileRequester(Requester):
    def post(self, model):
        # Заглушка для абстрактного метода post
        raise NotImplementedError("POST method not implemented for CustomerProfileRequester")

    def get(self) -> CustomerProfileResponse:
        url = f'{self.base_url}/customer/profile'
        response = requests.get(url=url, headers=self.headers)
        self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            return CustomerProfileResponse(**response.json())
        raise AssertionError(f'Unexpected status code: {response.status_code}, body: {response.text}')

    def put(self, change_name_user_request: ChangeNameUserRequest) -> ChangeNameUserResponse:
        url = f'{self.base_url}/customer/profile'
        response = requests.post(url=url, json=change_name_user_request.model_dump(), headers=self.headers)
        self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            return ChangeNameUserResponse(**response.json())
        raise AssertionError(f'Unexpected status code: {response.status_code}, body: {response.text}')
