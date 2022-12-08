import pika
import os
import time
import multiprocessing
import json
import requests
import random

from security.crypt import Cipher


class Sensor(multiprocessing.Process):
    def __init__(self, type):
        multiprocessing.Process.__init__(self)
        self.type = type

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
                print(
                    f"[Sensor-{self.type}]Cannot connect to RabbitMQ. Retrying in 15 seconds"
                )
                time.sleep(15)

        while True:
            data = self.encrypt_data(self.generate_data())

            print(data)

            channel.basic_publish(
                exchange="uma", routing_key=f"sensors", body=json.dumps(data)
            )
            time.sleep(10)

    def get_value(self, normal_min, normal_max, range_min, range_max):
        if random.randint(1, 100) > 97:
            # value in range
            return round(random.uniform(range_min, range_max), 2)
        else:
            # normal value
            return round(random.uniform(normal_min, normal_max), 2)

    def encrypt_data(self, data:dict) -> dict:
        key = os.getenv("APP_KEY_INVERNADERO")
        cipher = Cipher(key)
        str_data = json.dumps(data, default=str)

        return cipher.encrypt(str_data)

    def generate_data(self):

        #Cuidado, si se cambian estos valores, cambiar tb en API!
        data_dict = {
            "temp": self.get_value(15, 20, -10, 45),
            "hum": self.get_value(65, 70, 0, 100),
            "water_ph": self.get_value(5.5, 6.5, 0, 14),
            "soil_ph": self.get_value(4.6, 6.5, 0, 14),
            "water_salinity": self.get_value(0.0, 1.0, 0, 5),
            "water_o2": self.get_value(4, 8, 2, 8),
        }

        return data_dict
