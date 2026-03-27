from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.skeleton.endpoint import Endpoint
from src.main.api.requests.skeleton.requesters.crud_requester import CrudRequester
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.admin_user_requester import AdminUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class AdminSteps(BaseSteps):
    def create_user(self, user_request: CreateUserRequest):
        create_user_response: CreateUserResponse = CrudRequester(
            RequestSpecs.admin_auth_spec(),
            Endpoint.ADMIN_USER,
            ResponseSpecs.entity_was_created()
        ).post(user_request)

        assert create_user_response.username == user_request.username
        assert create_user_response.role == user_request.role

        self.created_objects.append(create_user_response)

        return create_user_response

    def delete_user(self, user_id: int):
        AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.entity_was_deleted()
        ).delete(user_id)

    def get_all_users(self):
        customer_profile = AdminUserRequester(
            RequestSpecs.admin_auth_spec(),
            ResponseSpecs.request_returns_ok()
        ).get()

        return customer_profile