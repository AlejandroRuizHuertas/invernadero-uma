import json

import pika
import os
import time
import multiprocessing

from security.crypt import Cipher


class Actuator(multiprocessing.Process):
    def __init__(self, type):
        multiprocessing.Process.__init__(self)
        self.type = type

    def run(self):
        connected = False
        channel = None
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
                    f"[Actuator-{self.type}]Cannot connect to RabbitMQ. Retrying in 15 seconds"
                )
                time.sleep(15)

        channel.basic_consume(
                queue='activators', on_message_callback=self.process_msg, auto_ack=True
            )
        print(f"I represent one actuator of type: {self.type}")
        print(f"[Actuator]Waiting commands")
        channel.start_consuming()

    #Recibimos str que representa json con cipher_data, mac, nonce
    def process_msg(self, ch, method, properties, body):

        key = os.getenv("APP_KEY_INVERNADERO")
        d = json.loads(body)

        cipher = Cipher(key)
        text = cipher.decrypt(
            bytes.fromhex(d['cipher_data']),
            bytes.fromhex(d['mac']),
            bytes.fromhex(d['nonce'])
        )


        # I guess we just show the msg
        print(text)
