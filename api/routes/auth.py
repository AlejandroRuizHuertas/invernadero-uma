from flask import Blueprint, request
from flask_cors import cross_origin
from helpers.response import error_response, success_response
from helpers.validate import validate_email_and_password, validate_user
from models.user import User

routes_auth = Blueprint("routes_auth", __name__)


# @routes_auth.route("/users/", methods=["POST"])
#Comentar esta funcion una vez creado el usuario
# def add_user():
#     try:
#         user = request.json
#         if not user:
#             return error_response("Please provide user details", "Bad request")
#         is_validated = validate_user(**user)
#         if is_validated is not True:
#             return error_response('Invalid data', is_validated)
#         user = User().create(**user)
#         if not user:
#             return error_response("User already exists", "Conflict", 409)
#         return success_response("Successfully created new user", user, 201)
#     except Exception as e:
#         return error_response("Something went wrong", str(e), 500)

def get_user():

    user = None

    try:
        data = request.json
        if not data:
            return error_response("Please provide user details", "Bad request")

        is_validated = validate_email_and_password(data.get('email'), data.get('password'))
        if is_validated is not True:
            return error_response("Invalid data", is_validated)

    except Exception as e:
        return error_response("Something went wrong!", str(e), 500)

    try:
        user = User().login(data["email"], data["password"])
    except Exception as e:
        return error_response("Error fetching auth token!, invalid email or password", "Unauthorized", 401)

    return user

def check_user_request(role):
    user = get_user()

    if type(user) is dict and '_id' in user and 'role' in user:
        if user['role'] == role:
            return success_response("Successfully fetched auth token", user)
        else:
            return error_response("El usuario no tiene permisos de {0}".format(role), "Forbbiden", 403)

    return user

@routes_auth.route("/users/login", methods=["POST"])
@cross_origin()
def login():
    return check_user_request('greenhouse')
@routes_auth.route("/admin/login", methods=["POST"])
@cross_origin()
def admin_login():
    return check_user_request('admin')
