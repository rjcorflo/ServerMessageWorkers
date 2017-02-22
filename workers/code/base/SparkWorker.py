# from pyspark.ml.feature import StringIndexer
import logging
# $example on$
from numpy import array
# from math import sqrt
from pyspark import SparkConf
# $example off$
from pyspark import SparkContext
# $example on$
from pyspark.mllib.clustering import KMeans, KMeansModel

print "Successfully imported Spark Modules"

class SparkWorker(object):
    """ Class for inheritance.

    Serve as base for inheritance.
    """
    def __init__(self, data=None, database=None, context=None):
        self.spark_context = context
        self.data = data
        self.database = database

    def update_task_status(self, status):
        """ Update task status.
        """
        result = self.database.tasks.update_one(
            {'identifier': self.data["identifier"]},
            {
                "$set": {
                    "status": status
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
        logging.error("DATA")
        logging.error(self.data)

        same_model = KMeansModel.load(self.spark_context, "/todo/resultadocluster")
        #data = array([0.0, 0.0, 1.0, 1.0, 9.0, 8.0, 8.0, 9.0]).reshape(4, 2)
	    #print(sameModel.computeCost(sc.parallelize(data)))
        resultado = str(same_model.clusterCenters)

        self.database.tasks.update_one(
            {'identifier': self.data["identifier"]},
            {
                "$set": {
                    "result": resultado
                }
            }
        )
