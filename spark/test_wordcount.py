from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import json

sc = SparkContext()
sql = SQLContext(sc)
stream = StreamingContext(sc, 1)  # 1 second window

kafka_stream = KafkaUtils.createStream(stream,
                                       'localhost:2181',
                                       'event_streaming_consumer',
                                       {"MyTopic": 1})


def analyze(grouping):
    print grouping
    # group_key = grouping[0]
    # group = grouping[1]
    # for doc in group:
    #     print doc
    return (None, grouping)


parsed = kafka_stream.map(lambda (k, v): json.loads(v))

red = parsed.map(analyze)
red.pprint()

stream.start()
stream.awaitTermination()
