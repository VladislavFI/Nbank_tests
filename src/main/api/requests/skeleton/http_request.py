from typing import Protocol


class HttpRequest(Protocol):
    def __init__(self):
        self.request_spec = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec