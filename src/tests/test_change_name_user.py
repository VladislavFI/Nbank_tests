import pytest
import requests
from src.main.api.models.change_name_user_request import ChangeNameUserRequest
from src.main.api.requests.customer_profile_requester import CustomerProfileRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestChangeNameUser:

    @pytest.mark.parametrize("customer_name", [
        "Ma_3-."
        "Maa",
        "Maa3",
        "Maa12345678912",
        "Maa123456789123",
        "Maa1234567891234",
        "AAAAA",
        "12345",
        "-----",
        "_____",
        "....."
    ])
    # Кейс: Изменение имени пользователем
    def test_change_name_user(self, customer_name):
        customer_profile_request = ChangeNameUserRequest(name=customer_name)

        # отправляем запрос на изменение имени
        customer_profile = CustomerProfileRequester(
            RequestSpecs.user_auth_spec("USER_2", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).put(customer_profile_request)


        # Запрос для проверки состояния пользователя после изменения
        customer_profile_after_change =  CustomerProfileRequester(
            RequestSpecs.user_auth_spec("USER_1", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).get()

        assert customer_profile_after_change.customer.name == customer_name


    @pytest.mark.parametrize("customer_name", [
        "Ma",
        "Maa12345678912344",
        ""
    ])
    @pytest.mark.debug
    # Кейс: Изменение имени пользователем (Негативный)
    def test_change_name_user_negative(self, customer_name):
        # Запрос для проверки состояния пользователя перед изменением
        customer_profile_before_change = CustomerProfileRequester(
            RequestSpecs.user_auth_spec("USER_1", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_ok()
        ).get()

        customer_profile_request = ChangeNameUserRequest(name=customer_name)

        # отправляем запрос на изменение имени
        customer_profile = CustomerProfileRequester(
            RequestSpecs.user_auth_spec("USER_1", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_bad_request()
        ).put(customer_profile_request)

        # Запрос для проверки состояния пользователя после изменения
        customer_profile_after_change =  CustomerProfileRequester(
            RequestSpecs.user_auth_spec("USER_1", "verysTRongPassword33$"),
            ResponseSpecs.request_returns_bad_request()
        ).get()

        assert (customer_profile_before_change["name"] ==
                customer_profile_after_change["name"])

