import pytest

from src.main.api.models.deposit_money_request import DepositMoneyRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.requests.deposit_money_requester import DepositMoneyRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.classes.api_manager import ApiManager

@pytest.mark.api
class TestDepositMoney:
    @pytest.mark.usefixtures("api_manager")
    @pytest.mark.parametrize("create_deposit_request", [
        DepositMoneyRequest(id=2, balance=100)])
    @pytest.mark.parametrize("username, password", [("USER_1", "verysTRongPassword33$")])
    # 1. Кейс: Депозит денег пользователем (Позитивный)
    def test_deposit_money(self, create_deposit_request: DepositMoneyRequest, api_manager: ApiManager, username: str,
                           password: str):
        # Получаем профиль до депозита
        customer_profile = api_manager.admin_steps.get_all_users()

        # Сохраняем старый баланс аккаунта
        old_balance = next(acc["balance"] for acc in customer_profile["accounts"]
                           if acc["id"] == create_deposit_request.id)

        # Делаем депозит
        response = api_manager.accounts_steps.deposit_money(create_deposit_request, username, password)

        # Запрос для проверки состояния пользователя после изменения
        customer_profile_after_change = api_manager.admin_steps.get_all_users()

        # Сохраняем новый баланс аккаунта
        new_balance = next(acc["balance"] for acc in
                           customer_profile_after_change["accounts"] if acc["id"] == create_deposit_request.id)

        # Проверка, что в ответе тот же id пользователя
        assert response.id == create_deposit_request.id

        # Проверка, что баланс пользователя увеличился
        assert new_balance == old_balance + create_deposit_request.balance

        # очистка данных
        #
        # AdminUserRequester(
        #     RequestSpecs.admin_auth_spec(),
        #     ResponseSpecs.entity_was_deleted()
        # ).delete(create_user_response.id)

    @pytest.mark.usefixtures("api_manager")
    @pytest.mark.parametrize("create_deposit_request", [
        DepositMoneyRequest(id=7, balance=150)])
    @pytest.mark.parametrize("username, password", [("USER_1", "verysTRongPassword33$")])
    # 2. Депозит денег на второй аккаунт пользователя
    def test_deposit_second_acc_user(self, create_deposit_request: DepositMoneyRequest, api_manager: ApiManager,
                                     username: str, password: str):

        # Получаем профиль до депозита
        customer_profile = api_manager.admin_steps.get_all_users()

        # Сохраняем старый баланс аккаунта
        old_balance_acc2 = next(acc["balance"] for acc in customer_profile["accounts"]
                                if acc["id"] == create_deposit_request.id)

        # Делаем депозит
        response = api_manager.accounts_steps.deposit_money(create_deposit_request, username, password)

        # Запрос для проверки состояния пользователя после изменения
        customer_profile_after_change = api_manager.admin_steps.get_all_users()

        # Новый баланс аккаунта
        new_balance_acc2 = next(acc["balance"] for acc in
                                customer_profile_after_change["accounts"] if
                                acc["id"] == create_deposit_request.id)

        # Проверка, что баланс пользователя увеличился
        assert new_balance_acc2 == old_balance_acc2 + create_deposit_request.balance

    @pytest.mark.usefixtures("api_manager")
    @pytest.mark.parametrize("create_deposit_request_non_exist", [
        DepositMoneyRequest(id=999, balance=150)])
    @pytest.mark.parametrize("username, password", [("USER_1", "verysTRongPassword33$")])
    # 3. Депозит денег на несуществующий аккаунт
    def test_deposit_non_exist_acc(self, create_deposit_request_non_exist,
                                  api_manager: ApiManager, username: str, password: str):
        # Проверка существующих счетов в банке
        user_profile = api_manager.admin_steps.get_all_users()

        valid_account_ids = [acc["id"] for acc in user_profile["accounts"]]

        assert create_deposit_request_non_exist.id not in valid_account_ids

        # Делаем депозит на несуществующий аккаунт
        response = api_manager.accounts_steps.deposit_money(create_deposit_request_non_exist,
                                                                       username, password)

    # 4 Депозит с неверным id
    @pytest.mark.parametrize("acc_id, expected_status", [
        ("1", 500),
        (None, 500)
    ])
    @pytest.mark.usefixtures("api_manager")
    @pytest.mark.parametrize("username, password", [("USER_1", "verysTRongPassword33$")])
    def test_deposit_invalid_id(self, acc_id, expected_status,
                                api_manager: ApiManager, username: str, password: str):
        # Проверка существующих счетов в банке

        user_profile = api_manager.admin_steps.get_all_users()

        valid_account_ids = [acc["id"] for acc in user_profile["accounts"]]

        assert acc_id not in valid_account_ids

        create_deposit_request = DepositMoneyRequest(id=acc_id, balance=100)

        # Делаем депозит c неверным id
        response = api_manager.accounts_steps.deposit_money(create_deposit_request,username, password)

    # 5 Депозит с неверным balance
    @pytest.mark.parametrize("deposit_sum, expected_status, expected_error", [
        (0, 400, "Invalid account or amount"),
        (-1, 400, "Invalid account or amount")
    ])
    @pytest.mark.usefixtures("api_manager")
    @pytest.mark.parametrize("username, password", [("USER_1", "verysTRongPassword33$")])
    def test_deposit_invalid_balance(self, deposit_sum, expected_status, expected_error,
                                api_manager: ApiManager, username: str, password: str):
        # Создаем запрос с некорректной суммой депозита
        create_deposit_request = DepositMoneyRequest(id=2, balance=deposit_sum)

        # Делаем депозит c неверным balance
        response =  api_manager.accounts_steps.deposit_money(create_deposit_request,username, password)

        # Проверка текста ошибки в ответе
        assert response.text.strip() == expected_error
