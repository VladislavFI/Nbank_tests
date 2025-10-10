import pytest
from src.main.api.models.transfer_money_request import TransferMoneyRequest
from src.main.api.requests.customer_profile_requester import CustomerProfileRequester
from src.main.api.requests.transfer_money_requester import TransferMoneyRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestTransferMoney:
    # 1. Перевод денег с одного аккаунта на другой
    def test_transfer_money(self):
        # Получаем данные об отправителе до перевода
        sender_profile = CustomerProfileRequester(
            RequestSpecs.user_auth_spec("USER_1", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).get()


        sender_transfer_request = TransferMoneyRequest(senderAccountId=5, receiverAccountId=4, amount=170)

        sender_balance_before = next(acc["balance"] for acc in sender_profile["accounts"]
                                   if acc["id"] == sender_transfer_request.senderAccountId)


        # Получаем данные о получателе до перевода
        receiver_profile = CustomerProfileRequester(
            RequestSpecs.user_auth_spec("USER_2", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).get()

        receiver_balance_before = next(acc["balance"] for acc in receiver_profile["accounts"]
                                     if acc["id"] == sender_transfer_request.receiverAccountId)


        # Выполняем перевод
        response = TransferMoneyRequester(
            RequestSpecs.user_auth_spec("USER_1", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).post(sender_transfer_request)

        # Проверяем, что ответ содержит информацию об обновленном аккаунте
        assert response.receiverAccountId == sender_transfer_request.receiverAccountId
        assert response.senderAccountId == sender_transfer_request.senderAccountId
        assert response.message == "Transfer successful"
        assert response.amount == sender_transfer_request.amount


        # Получаем данные об отправителе после перевода
        sender_profile_after = CustomerProfileRequester(
            RequestSpecs.user_auth_spec("USER_1", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).get()

        sender_balance_after = next(acc["balance"] for acc in sender_profile_after["accounts"]
                                  if acc["id"] == sender_transfer_request.senderAccountId)

        # Получаем данные о получателе после перевода
        receiver_profile_after = CustomerProfileRequester(
            RequestSpecs.user_auth_spec("USER_2", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).get()

        receiver_balance_after = next(acc["balance"] for acc in receiver_profile_after["accounts"]
                                    if acc["id"] == sender_transfer_request.receiverAccountId)

        # Проверяем, что баланс отправителя уменьшился на сумму перевода
        assert sender_balance_after == sender_balance_before - sender_transfer_request.amount
        # Проверяем, что баланс получателя увеличился на сумму перевода
        assert receiver_balance_after == receiver_balance_before + sender_transfer_request.amount

        # 2. Негативный тест: Перевод денег на несуществующий аккаунт
    def test_transfer_money_to_nonexistent_account(self):
        transfer_request = TransferMoneyRequest(senderAccountId=5,receiverAccountId=10,amount=50)
        # Выполняем перевод на несуществующий аккаунт
        response = TransferMoneyRequester(
            RequestSpecs.user_auth_spec("USER_1", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_bad_request("error",
                                                      "Invalid transfer:"
                                                      " insufficient funds or invalid accounts")
        ).post(transfer_request)