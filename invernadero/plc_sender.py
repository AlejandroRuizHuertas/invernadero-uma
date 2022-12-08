import pika
import os
import time
import json
import multiprocessing
import requests
from os import getenv

from security.crypt import Cipher


class PLCSENDER(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.token = None

    def run(self):
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
            except:
                print("[PLC]Cannot connect to RabbitMQ. Retrying in 15 seconds")
                time.sleep(15)

        channel.basic_consume(
            queue="sensors", on_message_callback=self.process_msg, auto_ack=True
        )
        print(f"I represent one PLC")

        user_json = {"email": os.getenv("APIUSER"), "password": os.getenv("APIPASS")}

        # login
        api_url = os.getenv("API_URL")
        r = requests.post(api_url+"users/login", json=user_json)
        print(r.status_code)
        self.token = r.json().get("data").get("token")
        print(f"Got token:{self.token}")
        print(f"[PLC]Waiting data")
        channel.start_consuming()

    def process_msg(self, ch, method, properties, body):
        api_url = os.getenv("API_URL")
        # here send the msg to the HTTP API
        print(f"[PLC]Got data:\n{body.decode()}")
        headers = {"Authorization": self.token}
        #desencriptar
        data = self.decrypt(body)

        print(f"Sending: {data}")
        result = requests.post(
            api_url+"greenhouse/send_data", json=data, headers=headers
        )
        print(f"Response: {result.text}")
        pass

    def decrypt(self, body:str) -> dict :
        key = os.getenv("APP_KEY_INVERNADERO")
        d = json.loads(body.decode())

        cipher = Cipher(key)
        text = cipher.decrypt(
            bytes.fromhex(d['cipher_data']),
            bytes.fromhex(d['mac']),
            bytes.fromhex(d['nonce'])
        )

        return json.loads(text)