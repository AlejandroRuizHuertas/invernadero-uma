from functools import wraps

from os import getenv

from helpers.response import error_response

from exceptions.exceptions import UserNotAuthorized


def role_x(f, current_user, role, args, kwargs):
    if current_user['role'] == role:
        return f(current_user, *args, **kwargs)

    raise UserNotAuthorized("El usuario no tiene permisos de {0}".format(role), current_user)

def role_greenhouse(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        return role_x(f, current_user, 'greenhouse', args, kwargs)

    return decorated

def role_admin(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        return role_x(f, current_user, 'admin', args, kwargs)

    return decorated
