import requests
from http import HTTPStatus

from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.models.deposit_money_response import DepositMoneyResponse
from src.main.api.requests.requester import Requester


class DepositMoneyRequester(Requester):
    def post(self, deposit_money_request: DepositMoneyRequest) -> DepositMoneyResponse:
        url = f'{self.base_url}/accounts/deposit'
        response = requests.post(url=url, json=deposit_money_request.model_dump(), headers=self.headers)
        self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            return DepositMoneyResponse(**response.json())
        raise AssertionError(f'Unexpected status code: {response.status_code}, body: {response.text}')