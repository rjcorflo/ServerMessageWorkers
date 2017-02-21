from base.base_worker import BaseWorker
# from pyspark.ml.feature import StringIndexer
# $example on$
from numpy import array
# from math import sqrt
from pyspark import SparkConf
# $example off$
from pyspark import SparkContext
# $example on$
from pyspark.mllib.clustering import KMeans, KMeansModel

print ("Successfully imported Spark Modules")

class SparkWorker(BaseWorker):
    def __proccess(self):
        sc = SparkContext("local", "Simple App")
        sameModel = KMeansModel.load(sc, "C:\Users\diego.alonso\Desktop\\resultadocluster")
        data = array([0.0, 0.0, 1.0, 1.0, 9.0, 8.0, 8.0, 9.0]).reshape(4, 2)
	    #print(sameModel.computeCost(sc.parallelize(data)))
        w = str(sameModel.clusterCenters)
        resultado = w 
