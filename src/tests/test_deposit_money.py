import pytest

from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.deposit_money_requester import DepositMoneyRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestDepositMoney:
    # 1. Кейс: Депозит денег пользователем (Позитивный)
    def test_deposit_money(self):
        # Получаем профиль до депозита
        customer_profile = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_ok()
        ).get()

        create_deposit_request = DepositMoneyRequest(id=2, balance=100)

        old_balance = next(acc["balance"] for acc in customer_profile["accounts"]
                           if acc["id"] == create_deposit_request.id)

        # Делаем депозит
        response = DepositMoneyRequester(
            RequestSpecs.user_auth_spec(username="USER_1", password="verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).post(create_deposit_request)


        # Запрос для проверки состояния пользователя после изменения
        customer_profile_after_change = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_ok()
        ).get()

        new_balance = next(acc["balance"] for acc in
                           customer_profile_after_change["accounts"] if acc["id"] == create_deposit_request.id)


        # Проверка, что в ответе тот же id пользователя
        assert response.id == create_deposit_request.id

        # Проверка, что баланс пользователя увеличился
        assert new_balance == old_balance + create_deposit_request.balance


        #очистка данных
        #
        # AdminUserRequester(
        #     RequestSpecs.admin_auth_spec(),
        #     ResponseSpecs.entity_was_deleted()
        # ).delete(create_user_response.id)

    # 2. Депозит денег на второй аккаунт пользователя
    def test_deposit_second_acc_user(self):
        # Получаем профиль до депозита
        customer_profile = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_ok()
        ).get()

        create_deposit_request = DepositMoneyRequest(id=7, balance=150)

        old_balance_acc2 = next(acc["balance"] for acc in customer_profile["accounts"]
                                if acc["id"] == create_deposit_request.id)

        # Делаем депозит
        response = DepositMoneyRequester(
            RequestSpecs.user_auth_spec(username="USER_1", password="verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).post(create_deposit_request)

        # Запрос для проверки состояния пользователя после изменения
        customer_profile_after_change = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_ok()
        ).get()

        new_balance_acc2 = next(acc["balance"] for acc in
                                customer_profile_after_change["accounts"] if
                                acc["id"] == create_deposit_request.id)


        # Проверка, что баланс пользователя увеличился
        assert new_balance_acc2 == old_balance_acc2 + create_deposit_request.balance

    # 3. Депозит денег на несуществующий аккаунт
    def test_deposit_non_exist_acc(self):
        # Проверка существующих счетов в банке
        user_profile = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_ok()
        ).get()

        create_deposit_request = DepositMoneyRequest(id=999, balance=150)

        valid_account_ids = [acc["id"] for acc in user_profile["accounts"]]

        assert create_deposit_request.id not in valid_account_ids

        # Делаем депозит на несуществующий аккаунт
        response = DepositMoneyRequester(
            RequestSpecs.user_auth_spec(username="USER_1", password="verysTRongPassword33$"),
            ResponseSpecs.request_returns_forbidden()
        ).post(create_deposit_request)

    # 4 Депозит с неверным id
    @pytest.mark.parametrize("acc_id, expected_status", [
        ("1", 500),
        (None, 500)
    ])
    def test_deposit_invalid_id(self, acc_id, expected_status):
        # Проверка существующих счетов в банке

        user_profile = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_ok()
        ).get()

        valid_account_ids = [acc["id"] for acc in user_profile["accounts"]]

        assert acc_id not in valid_account_ids

        create_deposit_request = DepositMoneyRequest(id=acc_id, balance=100)

        # Делаем депозит c неверным id
        response = DepositMoneyRequester(
            RequestSpecs.user_auth_spec(username="USER_1", password="verysTRongPassword33$"),
            ResponseSpecs.request_returns_status(expected_status)
        ).post(create_deposit_request)

    # 5 Депозит с неверным balance
    @pytest.mark.parametrize("deposit_sum, expected_status, expected_error", [
        (0, 400, "Invalid account or amount"),
        (-1, 400, "Invalid account or amount")
    ])
    def test_deposit_invalid_balance(self, deposit_sum, expected_status, expected_error):
        # Создаем запрос с некорректной суммой депозита
        create_deposit_request = DepositMoneyRequest(id=2, balance=deposit_sum)

        # Делаем депозит c неверным balance
        response = DepositMoneyRequester(
            RequestSpecs.user_auth_spec(username="USER_1", password="verysTRongPassword33$"),
            ResponseSpecs.request_returns_status(expected_status, expected_error)
        ).post(create_deposit_request)

        # Проверка текста ошибки в ответе
        assert response.text.strip() == expected_error
