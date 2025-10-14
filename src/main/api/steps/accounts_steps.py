from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.requests.deposit_money_requester import DepositMoneyRequester
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.models.transfer_money_response import TransferMoneyResponse
from src.main.api.requests.transfer_money_requester import TransferMoneyRequester

from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps

class AccountsSteps(BaseSteps):
    def deposit_money(self, deposit_money_request: DepositMoneyRequest, username: str, password: str):
        deposit_money_response = DepositMoneyRequester(
            RequestSpecs.user_auth_spec(username, password),
            ResponseSpecs.request_returns_ok()
        ).post(deposit_money_request)

        return deposit_money_response

    def transfer_money(self, transfer_money_request: TransferMoneyRequest, username: str, password: str):
        transfer_money_response = TransferMoneyRequester(
            RequestSpecs.user_auth_spec(username, password),
            ResponseSpecs.request_returns_ok()
        ).post(transfer_money_request)

        return transfer_money_response