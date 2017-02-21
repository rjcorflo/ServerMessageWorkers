#!/usr/bin/env python
import json
import pika
from pymongo import MongoClient
from base.base_worker import BaseWorker
from base.constantes import MONGO_HOST, MONGO_PORT, RABBIT_HOST, RABBIT_PORT

class MainWorker(object):
    """ Main class

    To start script.
    """
    def __init__(self):
        client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.database = client.mydatabase


    def run(self):
        """ Run script """
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT))
        channel = connection.channel()

        channel.queue_declare(queue='task_queue', durable=True)
        print ' [*] Waiting for messages. To exit press CTRL+C'

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback, queue='task_queue')

        channel.start_consuming()


    def launch(self, worker=BaseWorker()):
        """ Launch worker """
        worker.launch_processing()


    def callback(self, canal, method, properties, body):
        """ Callback for task process """
        print " [x] Received task"
        # Get data
        data = json.loads(body)
        # Init and launch worker
        worker = BaseWorker(data=data, database=self.database)
        self.launch(worker)
        # Acknowledge task processing
        print " [x] Done"
        canal.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    MainWorker().run()
