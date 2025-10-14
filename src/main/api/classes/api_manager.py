from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.accounts_steps import AccountsSteps
from src.main.api.steps.customer_steps import CustomerSteps


class ApiManager:
    def __init__(self, created_objects: list):
        self.admin_steps = AdminSteps(created_objects)
        self.accounts_steps = AccountsSteps(created_objects)
        self.customer_steps = CustomerSteps (created_objects)