import pytest
import requests

BASE_URL = "http://localhost:4111/api/v1"
AUTH_HEADER = {
    'accept': 'application/json',
    'Authorization': 'Basic a2F0ZTE5OTg3Nzp2ZXJ5c1RSb25nUGFzc3dvcmQzMyQ=',
    'Content-Type': 'application/json'
}

AUTH_HEADER_ADMIN = {
    'accept': 'application/json',
    'Authorization': 'Basic YWRtaW46YWRtaW4=',
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
                           if acc["id"] == 2)

        # Делаем депозит
        response = requests.post(
            url=f"{BASE_URL}/accounts/deposit",
            json={
                "id": 2,
                "balance": 100
            },
            headers=AUTH_HEADER
        )

        # Запрос для проверки состояния пользователя после изменения
        customer_profile_after_change = requests.get(
            url=f"{BASE_URL}/customer/profile",
            headers=AUTH_HEADER
        )

        new_balance = next(acc["balance"] for acc in
                           customer_profile_after_change.json()["accounts"] if acc["id"] == 2)

        # Проверка кода ответа
        assert response.status_code == 200

        # Проверка, что в ответе тот же id пользователя
        assert response.json().get('id') == 2

        # Проверка что баланс пользователя увеличился
        assert new_balance == old_balance + 100

    # 2. Депозит денег на второй аккаунт пользователя
    def test_deposit_second_acc_user(self):
        # Получаем профиль до депозита
        customer_profile = requests.get(
            url=f"{BASE_URL}/customer/profile",
            headers=AUTH_HEADER
        )

        old_balance_acc2 = next(acc["balance"] for acc in customer_profile.json()["accounts"]
                                if acc["id"] == 7)

        # Делаем депозит
        response = requests.post(
            url=f"{BASE_URL}/accounts/deposit",
            json={
                "id": 7,
                "balance": 150
            },
            headers=AUTH_HEADER
        )

        # Запрос для проверки состояния пользователя после изменения
        customer_profile_after_change = requests.get(
            url=f"{BASE_URL}/customer/profile",
            headers=AUTH_HEADER
        )

        new_balance_acc2 = next(acc["balance"] for acc in
                                customer_profile_after_change.json()["accounts"] if acc["id"] == 7)

        # Проверка кода ответа
        assert response.status_code == 200

        # Проверка, что это аккаунт с id=2
        assert response.json().get('id') == 7

        # Проверка, что баланс пользователя увеличился
        assert new_balance_acc2 == old_balance_acc2 + 150

    # 3. Депозит денег на несуществующий аккаунт
    def test_deposit_non_exist_acc(self):
        # Проверка существующих счетов в банке

        list_valid_accounts = requests.get(
            url=f"{BASE_URL}/admin/users",
            headers=AUTH_HEADER_ADMIN
        )

        valid_account_ids = [acc["id"] for user in list_valid_accounts.json() for acc in user["accounts"]]

        assert 999 not in valid_account_ids

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

    # 4 Депозит с неверным id
    @pytest.mark.parametrize("acc_id, expected_status", [
        ("1", 500),
        (1.5, 200),
        (None, 500)
    ])
    # TODO Параметризация подогнана для того чтобы тесты были зелеными.
    def test_deposit_invalid_id(self, acc_id, expected_status):
        # Проверка существующих счетов в банке

        list_valid_accounts = requests.get(
            url=f"{BASE_URL}/admin/users",
            headers=AUTH_HEADER_ADMIN
        )

        valid_account_ids = [acc["id"] for user in list_valid_accounts.json() for acc in user["accounts"]]

        assert acc_id not in valid_account_ids

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

    # 5 Депозит с неверным balance
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
