import pytest
import requests

BASE_URL= "http://localhost:4111/api/v1"
AUTH_SENDER_HEADER = {
    'accept': 'application/json',
    'Authorization': 'Basic dXNlcl8xX21heDp2ZXJ5c1R3ZGF3ZDMzMTIzMTIk',
    'Content-Type': 'application/json'
}

AUTH_RECEIVER_HEADER = {
    'accept': 'application/json',
    'Authorization': 'Basic dXNlcl8yX25pY2s6dmVyeXNUd2Rhd2QzMyQ=',
    'Content-Type': 'application/json'
}


@pytest.mark.api
class TestTransferMoney:
    # 1. Перевод денег с одного аккаунта на другой
    def test_transfer_money(self):
        # Получаем данные об отправителе до перевода
        sender_profile = requests.get(
            url=f"{BASE_URL}/customer/profile",
            headers=AUTH_SENDER_HEADER
        )
        sender_balance_before = next(acc["balance"] for acc in sender_profile.json()["accounts"]
                                   if acc["id"] == 5)


        # Получаем данные о получателе до перевода
        receiver_profile = requests.get(
            url=f"{BASE_URL}/customer/profile",
            headers=AUTH_RECEIVER_HEADER
        )
        receiver_balance_before = next(acc["balance"] for acc in receiver_profile.json()["accounts"]
                                     if acc["id"] == 4)

        # Выполняем перевод
        response = requests.post(
            url=f"{BASE_URL}/accounts/transfer",
            json={
                "senderAccountId": 5,
                "receiverAccountId": 4,
                "amount": 170
            },
            headers=AUTH_SENDER_HEADER
        )

        # Проверяем код ответа
        assert response.status_code == 200

        # Проверяем, что ответ содержит информацию об обновленном аккаунте
        response_data = response.json()
        assert response_data.get('receiverAccountId') == 4
        assert response_data.get('senderAccountId') == 5
        assert response_data.get('message') == "Transfer successful"
        assert response_data.get('amount') == 170


        # Получаем данные об отправителе после перевода
        sender_profile_after = requests.get(
            url=f"{BASE_URL}/customer/profile",
            headers=AUTH_SENDER_HEADER
        )
        sender_balance_after = next(acc["balance"] for acc in sender_profile_after.json()["accounts"]
                                  if acc["id"] == 5)

        # Получаем данные о получателе после перевода
        receiver_profile_after = requests.get(
            url=f"{BASE_URL}/customer/profile",
            headers=AUTH_RECEIVER_HEADER
        )
        receiver_balance_after = next(acc["balance"] for acc in receiver_profile_after.json()["accounts"]
                                    if acc["id"] == 4)

        # Проверяем, что баланс отправителя уменьшился на сумму перевода
        assert sender_balance_after == sender_balance_before - 170
        # Проверяем, что баланс получателя увеличился на сумму перевода
        assert receiver_balance_after == receiver_balance_before + 170

        # 2. Негативный тест: Перевод денег на несуществующий аккаунт
    def test_transfer_money_to_nonexistent_account(self):
        # Выполняем перевод на несуществующий аккаунт
        response = requests.post(
            url=f"{BASE_URL}/accounts/transfer",
            json={
                "senderAccountId": 5,
                "receiverAccountId": 10,
                "amount": 50
            },
            headers=AUTH_SENDER_HEADER
        )

        # Проверяем код ответа
        assert response.status_code == 400

        # Проверяем, что ответ содержит сообщение об ошибке
        response_data = response.text.strip() == "Invalid transfer: insufficient funds or invalid accounts"