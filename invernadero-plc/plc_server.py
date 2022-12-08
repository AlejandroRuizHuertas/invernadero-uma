import pika
import os
import time
import json
import multiprocessing
import requests
import threading

from flask import Flask, request

app = Flask(__name__)
plc_server = None


@app.before_first_request
def before_first_request():
    global plc_server
    plc_server = PLCSERVER()


# TODO: Toda esta informacion tiene que ir cifrada
@app.route("/activator/riego", methods=["POST"])
def activator_endpoint():
    response = {"message": "success"}
    global plc_server

    try:
        plc_server.edit_activator(request.get_json())
    except pika.exceptions.AMQPConnectionError:
        response = {"error": True, "message": "Error de conexion PIKA"}


    #TODO: No me gusta, que en caso de que haya un error en el receptor, no nos enteramos
    # me refiero a un error diferente de AMQP Connection



    return response, 200


@app.route("/ver", methods=["GET"])
def ver():
    response = {"ver": "1.0"}
    return response, 200


def run_server():
    global plc_server
    plc_server = PLCSERVER()
    app.run(host="0.0.0.0", port=5000)


class PLCSERVER:
    def __init__(self):
        self.channel = self.get_channel()

    def get_channel(self):
        connected = False
        while not connected:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        "172.5.0.6",
                        5672,
                        "/",
                        pika.PlainCredentials(
                            os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASS")
                        ),
                    )
                )
                channel = connection.channel()
                connected = True
            except pika.exceptions.AMQPConnectionError:
                print(
                    f"[Sensor-{'##self.type##'}]Cannot connect to RabbitMQ. Retrying in 15 seconds"
                )
                time.sleep(15)
        return channel

    # por request, recibimos json con los siguientes campos:
    # cipher_data, mac, nonce
    # idelamente, podria desencriptar la informacion aqui,
    # y usar ssl en rabbitmq
    # pero como temo que eso no va a ser trivial...
    # simplemente hacemos de puente aqui y se desencripta en plc_sensor
    def edit_activator(self, data: dict):
        str_data = json.dumps(data)
        print(f"[PLC]Sending {str_data}")
        self.channel.basic_publish(
            exchange="uma", routing_key=f"activators", body=str_data
        )
