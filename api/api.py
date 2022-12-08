import json
from datetime import datetime
from os import getenv

import bson.errors
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, request

import requests

from models.log_msg import LogMsg
from helpers.anomalies import setAnomalies, scan, setAnomaly
from security.InvernaderoDataScanner import InvernaderoDataScanner
from exceptions.exceptions import UnauthorizedRequestException, UserNotActive, UserNotAuthorized, BadRequestException
from security.crypt import Cipher
from middlewares.permissions import role_admin, role_greenhouse
from form_requests.send_greenhouse_data_request import SendGreenHouseDataRequest
from middlewares.auth import token_required
from models.greenhouse_data import GreenHouseData
from models.user import User
from helpers.response import error_response, success_response
from routes.auth import routes_auth
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(routes_auth)


@app.errorhandler(UnauthorizedRequestException)
def prueba_except(err):
    ip = request.remote_addr
    dt = datetime.now()
    user = None
    setAnomaly(err.long_msg, "NOTICE", ip, dt, user)
    return error_response(err.long_msg, err.short_msg, err.http_code)


@app.errorhandler(UserNotActive)
def prueba_except(err):
    ip = request.remote_addr
    dt = datetime.now()
    user = err.user
    setAnomaly(err.long_msg, "NOTICE", ip, dt, user)
    return error_response(err.long_msg, err.short_msg, err.http_code)


@app.errorhandler(UserNotAuthorized)
def prueba_except(err):
    ip = request.remote_addr
    dt = datetime.now()
    user = err.user
    setAnomaly(err.long_msg, "WARNING", ip, dt, user)
    return error_response(err.long_msg, err.short_msg, err.http_code)


@app.errorhandler(BadRequestException)
def prueba_except(err):
    ip = request.remote_addr
    dt = datetime.now()
    user = None
    setAnomaly(err.long_msg, "WARNING", ip, dt, user)
    return error_response(err.long_msg, err.short_msg, err.http_code)


@app.route('/greenhouse/send_data', methods=["POST"])
@token_required
@role_greenhouse
def send_data(user: User):
    try:
        validated = SendGreenHouseDataRequest().validated()
    except Exception:
        raise BadRequestException("Error al obtener datos recibidos", user)

    try:
        ip = request.remote_addr
        dt = datetime.now()

        validated = {
            **validated,
            "created": dt,
            "ip": ip,
            'user': {
                "_id": ObjectId(user['_id']),
                "name": user['name'],
            }
        }

        #detecta anomalias
        scanner = InvernaderoDataScanner()
        scan(scanner, validated, ip, dt, user)

        ghd = GreenHouseData().insert(validated)

        return success_response("GHD stored", ghd)
    except Exception as e:
        return error_response("Something went wrong!", str(e), 500)

    return error_response("Something went wrong!", "", 500)


@app.route('/greenhouse/avg_data', methods=["GET"])
@token_required
@role_admin
def greenhouse_avg_data(user):
    model = GreenHouseData()
    return success_response("", model.avg())


@app.route('/greenhouses', methods=["GET"])
@token_required
@role_admin
def greenhouse_list(user):
    model = User()
    return success_response("", model.findAll(
        {
            "role": "greenhouse"
        }
    ))


@app.route('/greenhouse/<id>/data', methods=["GET"])
@token_required
@role_admin
def greenhouse_history(user, id):
    model = GreenHouseData()
    return success_response("", model.history(id))


@app.route('/greenhouse/<id>/do_action/irrigation', methods=["POST"])
@token_required
@role_admin
def greenhouse_open_window(user, id):
    riego = request.get_json().get("riego", False)

    try:
        invernadero = User().get_by_id(id)
    except Exception:
        return error_response("Error: Invernadero desconocido", "Error", 404)

    params = __get_cipher_irrigation_data(riego)
    endpoint = "{0}/activator/riego".format(invernadero['endpoint'])

    # endpoint = "http://invernadero-plc:5000/activator/riego"

    try:
        result = requests.post(
            endpoint, json=params, headers={}
        )

        if result.status_code == 200:
            return result.json(), 200

    except requests.exceptions.ConnectionError:
        return error_response("Error de conexion invernadero", "Error", 500)

    return error_response("Error inesperado envio señal invernadero", "Error", 500)


@app.route('/anomalias', methods=["GET"])
@token_required
@role_admin
def anomalias(user):
    return success_response("", LogMsg().history())


def __get_irrigation_data(riego: bool) -> dict:
    return {
        'riego': riego,
        'date': datetime.now()
    }


def __get_cipher_irrigation_data(riego: bool) -> dict:
    data = __get_irrigation_data(riego)
    str_data = json.dumps(data, default=str)

    key = getenv("APP_KEY_INVERNADERO")
    cipher = Cipher(key)
    return cipher.encrypt(str_data)
