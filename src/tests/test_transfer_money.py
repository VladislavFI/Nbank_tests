import pytest

from src.conftest import ApiManager, api_manager
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.requests.customer_profile_requester import CustomerProfileRequester
from src.main.api.requests.transfer_money_requester import TransferMoneyRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestTransferMoney:
    @pytest.mark.parametrize("sender_transfer_request", [
        TransferMoneyRequest(senderAccountId=5, receiverAccountId=4, amount=170)])
    @pytest.mark.usefixtures("api_manager")
    @pytest.mark.parametrize("username1, password1", [("USER_1", "verysTRongPassword33$")])
    @pytest.mark.parametrize("username2, password2", [("USER_1", "verysTRongPassword33$")])
    # 1. Перевод денег с одного аккаунта на другой
    def test_transfer_money(self, sender_transfer_request, api_manager: ApiManager, username1: str, password1: str,
                            username2: str, password2: str):

        # Получаем данные об отправителе до перевода
        sender_profile = api_manager.customer_steps.get_customer_profile(username1, password1)

        #  Сохраняем старый баланс аккаунта отправителя
        sender_balance_before = next(acc["balance"] for acc in sender_profile["accounts"]
                                   if acc["id"] == sender_transfer_request.senderAccountId)


        # Получаем данные о получателе до перевода
        receiver_profile = api_manager.customer_steps.get_customer_profile(username2, password2)

        # Сохраняем старый баланс аккаунта получателя
        receiver_balance_before = next(acc["balance"] for acc in receiver_profile["accounts"]
                                     if acc["id"] == sender_transfer_request.receiverAccountId)


        # Выполняем перевод
        response = api_manager.accounts_steps.transfer_money(sender_transfer_request, username1, password1)


        # Проверяем, что ответ содержит информацию об обновленном аккаунте
        assert response.receiverAccountId == sender_transfer_request.receiverAccountId
        assert response.senderAccountId == sender_transfer_request.senderAccountId
        assert response.message == "Transfer successful"
        assert response.amount == sender_transfer_request.amount


        # Получаем данные об отправителе после перевода
        sender_profile_after = api_manager.customer_steps.get_customer_profile(username1, password1)

        sender_balance_after = next(acc["balance"] for acc in sender_profile_after["accounts"]
                                  if acc["id"] == sender_transfer_request.senderAccountId)

        # Получаем данные о получателе после перевода
        receiver_profile_after = api_manager.customer_steps.get_customer_profile(username2, password2)

        receiver_balance_after = next(acc["balance"] for acc in receiver_profile_after["accounts"]
                                    if acc["id"] == sender_transfer_request.receiverAccountId)

        # Проверяем, что баланс отправителя уменьшился на сумму перевода
        assert sender_balance_after == sender_balance_before - sender_transfer_request.amount
        # Проверяем, что баланс получателя увеличился на сумму перевода
        assert receiver_balance_after == receiver_balance_before + sender_transfer_request.amount

        # 2. Негативный тест: Перевод денег на несуществующий аккаунт
    @pytest.mark.usefixtures("api_manager")
    @pytest.mark.parametrize("creds", [("USER_1", "verysTRongPassword33$")])
    def test_transfer_money_to_nonexistent_account(self, api_manager: ApiManager, creds):
        transfer_request = TransferMoneyRequest(senderAccountId=5,receiverAccountId=10,amount=50)
        # Выполняем перевод на несуществующий аккаунт

        api_manager.accounts_steps.transfer_money(transfer_request, creds)