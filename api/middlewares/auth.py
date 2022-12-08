from functools import wraps

from flask import request, abort
from jwt import decode, exceptions
from os import getenv

from exceptions.exceptions import UnauthorizedRequestException

from models.user import User


def __get_token() -> str | None:
    return request.headers["Authorization"] if "Authorization" in request.headers else None


def __validate_token(token: str) -> User:
    secret = getenv("APP_KEY")
    algorithm = getenv("APP_ALGORITHM")

    try:
        data = decode(token, secret, algorithms=[algorithm])
    except exceptions.DecodeError:
        raise UnauthorizedRequestException("Invalid Authentication token!")
    except exceptions.ExpiredSignatureError:
        raise UnauthorizedRequestException("Token Expired!")

    if type(data) is not dict or "user_id" not in data or "exp" not in data:
        raise UnauthorizedRequestException("user_id and/or expiration_date(exp) missing!")

    current_user = User().get_by_id(data["user_id"])

    if current_user is None:
        raise UnauthorizedRequestException("User not in database")

    return current_user


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = __get_token()
        if not token:
            return UnauthorizedRequestException("Authentication Token is missing!")

        current_user = __validate_token(token)

        if not current_user["active"]:
            raise UserNotActive(current_user)


        return f(current_user, *args, **kwargs)

    return decorated
