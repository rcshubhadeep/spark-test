from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession


def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print ("Error")
        sys.exit(1)

    host, port = sys.argv[1:]
    sc = SparkContext(appName="PythonStreamingNetworkWordCount")
    ssc = StreamingContext(sc, 1)
    lines = ssc.socketTextStream(host, int(port))
    words = lines.flatMap(lambda line: line.split(" "))

    def process(time, rdd):
        print("========= %s =========" % str(time))
        try:
            spark = getSparkSessionInstance(rdd.context.getConf())
            rowRdd = rdd.map(lambda w: Row(word=w))
            wordsDataFrame = spark.createDataFrame(rowRdd)
            wordsDataFrame.createOrReplaceTempView("words")
            wordCountsDataFrame = spark.sql("select word, count(*) as total from words group by word")
            wordCountsDataFrame.show()
        except:
            pass

    words.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()
