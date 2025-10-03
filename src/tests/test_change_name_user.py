import pytest
import requests

BASE_URL = "http://localhost:4111/api/v1"
AUTH_HEADER = {
    'accept': 'application/json',
    'Authorization': 'Basic RmlsaXBfU006dmVyeXMxMTFFVFJvbmdQYXNzd29yZDMzJA==',
    'Content-Type': 'application/json'
}


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
        # отправляем запрос на изменение имени
        customer_profile = requests.put(
            url=f"{BASE_URL}/customer/profile",
            json={
                "name": customer_name
            },
            headers=AUTH_HEADER
        )

        assert customer_profile.status_code == 200
        assert customer_profile.json()["customer"]["name"] == customer_name

    @pytest.mark.parametrize("customer_name", [
        "Ma",
        "Maa12345678912344",
        ""
    ])
    @pytest.mark.debug
    # Кейс: Изменение имени пользователем (Негативный)
    def test_change_name_user_negative(self, customer_name):
        # отправляем запрос на изменение имени
        customer_profile = requests.put(
            url=f"{BASE_URL}/customer/profile",
            json={
                "name": customer_name
            },
            headers=AUTH_HEADER
        )

        assert customer_profile.status_code == 400

