from models.user import User


class UnauthorizedRequestException(Exception):
    http_code = 401
    short_msg = 'Unauthorized'
    error_type = 'Warning'
    long_msg = ''

    def __init__(self, long_msg: str):
        super().__init__()
        self.long_msg = long_msg


class UserNotActive(Exception):
    http_code = 403
    short_msg = 'Forbbiden'
    error_type = 'Warning'
    long_msg = 'User not activated'
    user = None

    def __init__(self, user: User):
        super().__init__()
        self.user = user


class UserNotAuthorized(Exception):
    http_code = 403
    short_msg = 'Forbbiden'
    error_type = 'Warning'
    long_msg = 'User not authorized'
    user = None

    def __init__(self, msg: str, user: User):
        super().__init__()
        self.long_msg = msg
        self.user = user

class BadRequestException(Exception):
    http_code = 500
    short_msg = 'Bad Request'
    error_type = 'Error'
    long_msg = ''
    user = None

    def __init__(self, msg: str, user: User):
        super().__init__()
        self.long_msg = msg
        self.user = user
