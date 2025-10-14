from src.main.api.requests.customer_profile_requester import CustomerProfileRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps



class CustomerSteps(BaseSteps):
    def get_customer_profile(self, username: str, password: str):
        customer_profile = CustomerProfileRequester(
            RequestSpecs.user_auth_spec(username, password),
            ResponseSpecs.request_returns_ok()
        ).get()

        return customer_profile
