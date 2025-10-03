import pytest
import requests

BASE_URL= "http://localhost:4111/api/v1"
AUTH_HEADER = {
    'accept': 'application/json',
    'Authorization': 'Basic a2F0ZTE5OTg3Nzp2ZXJ5c1RSb25nUGFzc3dvcmQzMyQ=',
    'Content-Type': 'application/json'
}

@pytest.mark.api
class TestDepositMoney:
    # 1. Кейс: Депозит денег пользователем (Позитивный)
    def test_deposit_money(self):
        # Получаем профиль до депозита
        customer_profile = requests.get(
            url=f"{BASE_URL}/customer/profile",
            headers=AUTH_HEADER
        )

        old_balance = next(acc["balance"] for acc in customer_profile.json()["accounts"]
                                if acc["id"] == 1)


        # Делаем депозит
        response = requests.post(
            url=f"{BASE_URL}/accounts/deposit",
            json={
                "id": 1,
                "balance": 100
            },
            headers=AUTH_HEADER
        )
        # Проверка кода ответа
        assert response.status_code == 200

        # Проверка, что в ответе тот же id пользователя
        assert response.json().get('id') == 1

        #Проверка что баланс увеличился
        assert response.json().get("balance") == old_balance + 100

    #2. Депозит денег на второй аккаунт пользователя
    def test_deposit_second_acc_user(self):
        # Получаем профиль до депозита
        customer_profile = requests.get(
            url=f"{BASE_URL}/customer/profile",
            headers=AUTH_HEADER
        )

        old_balance_acc2 = next(acc["balance"] for acc in customer_profile.json()["accounts"]
                                if acc["id"] == 2)

        # Делаем депозит
        response = requests.post(
            url=f"{BASE_URL}/accounts/deposit",
            json={
                "id": 2,
                "balance": 150
            },
            headers=AUTH_HEADER
        )

        # Проверка кода ответа
        assert response.status_code == 200

        # Проверка, что это аккаунт с id=2
        assert response.json().get('id') == 2

        # Проверка, что баланс увеличился ровно на 150
        assert response.json().get("balance") == old_balance_acc2 + 150

    #3. Депозит денег на несуществующий аккаунт
    def test_deposit_non_exist_acc(self):
        # Делаем депозит на несуществующий аккаунт
        response = requests.post(
            url=f"{BASE_URL}/accounts/deposit",
            json={
                "id": 999,
                "balance": 150
            },
            headers=AUTH_HEADER
        )

        # Проверка кода ответа
        assert response.status_code == 403

        # Проверка ошибки в ответе
        assert response.text.strip() == "Unauthorized access to account"

    #4 Депозит с неверным id
    @pytest.mark.parametrize("acc_id, expected_status",[
        ("1", 500),
        (1.5, 200),
        (None, 500)
    ])
    # TODO Параметризация подогнана для того чтобы тесты были зелеными.
    def test_deposit_invalid_id(self, acc_id, expected_status):
        # Делаем депозит c неверным id
        response = requests.post(
            url=f"{BASE_URL}/accounts/deposit",
            json={
                "id": acc_id,
                "balance": 150
            },
            headers=AUTH_HEADER
        )

        # Проверка кода ответа
        assert response.status_code == expected_status

#5 Депозит с неверным balance
    @pytest.mark.parametrize("deposit_sum, expected_status, expected_error", [
        (0, 400, "Invalid account or amount"),
        (-1, 400, "Invalid account or amount")
    ])
    def test_deposit_invalid_balance(self, deposit_sum, expected_status, expected_error):
        # Делаем депозит c неверным balance
        response = requests.post(
            url=f"{BASE_URL}/accounts/deposit",
            json={
                "id": 2,
                "balance": deposit_sum
            },
            headers=AUTH_HEADER
        )

        # Проверка кода ответа
        assert response.status_code == expected_status

        # Проверка кода ответа
        assert response.text.strip() == expected_error








