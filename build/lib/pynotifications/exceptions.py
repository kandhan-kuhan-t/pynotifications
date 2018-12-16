

class CallbackFailure(Exception):
    def __init__(self, message: str):
        super(CallbackFailure, self).__init__()
        self.message = message


class ResponseNot200(Exception):
    def __init__(self, message: str, status_code: str="NOT_PROVIDED"):
        super(ResponseNot200, self).__init__()
        self.message = message
        self.status_code = status_code


class NoConnection(Exception):
    def __init__(self, message: str, status_code="200"):
        super(NoConnection, self).__init__()
        self.message = message
        self.status_code = status_code


class SchemaError(Exception):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message
