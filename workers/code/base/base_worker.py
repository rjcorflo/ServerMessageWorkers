#!/usr/bin/env python
import time
import logging
import json
import random
import pika
from pymongo import MongoClient

class BaseWorker(object):
    """ Class for inheritance.

    Serve as base for inheritance.
    """
    def __init__(self, data=None, database=None):
        self.data = data
        self.database = database

    def update_task_status(self, status):
        """ Update task status.
        """
        result = self.database.tasks.update_one(
            {'identifier': self.data["identifier"]},
            {
                "$set": {
                    "status": status,
                    "result": ""
                }
            }
        )
        logging.error("Actualizados " + str(result.matched_count))

    def launch_processing(self):
        """ Process data.
        """
        self.update_task_status("IN-PROCCESS")
        self.__proccess()
        self.update_task_status("FINISHED")

    def __proccess(self):
        """ Method to be overriden

        Should use self.data to access data to be processed.
        """
        valor_random = random.randint(5, 15)
        time.sleep(valor_random)
        self.database.tasks.update_one(
            {'identifier': self.data["identifier"]},
            {
                "$set": {
                    "result": str(valor_random)
                }
            }
        )
