#!/usr/bin/env python
import time
import logging
import json
import random
import pika
from pymongo import MongoClient

client = MongoClient(
    "192.168.99.100",
    27017)
db = client.mydatabase


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="192.168.99.100", port=5672))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] Received task"

    # Recuperamos datos
    received_message = json.loads(body)
    # Ponemos tarea en proceso
    update_task_status(received_message["identifier"], "IN-PROCCESS")

    # Procesamos tarea
    proccess_prediction(received_message["data"])

    # Finalizamos tarea
    update_task_status(received_message["identifier"], "FINISHED")
    print " [x] Done"
    ch.basic_ack(delivery_tag=method.delivery_tag)


def update_task_status(identifier, status):
    result = db.mydatabase.update_one(
        {'identifier': identifier},
        {
            "$set": {
                "status": status,
                "result": "Texto indefinido"
            }
        }
    )

    logging.error("Actualizados" + str(result.matched_count))


def proccess_prediction(data):
    valor_random = random.randint(5, 15)
    time.sleep(valor_random)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')

channel.start_consuming()
