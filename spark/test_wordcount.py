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
    print type(grouping)
    return (None, grouping)
    # data_dict = grouping[1]
    # if 'event_type' not in data_dict:
    #     return (None, None)
    #
    # return (data_dict['event_type'], grouping)


parsed = kafka_stream.map(lambda (k, v): json.loads(v))

red = parsed.map(analyze)
red.pprint()

stream.start()
stream.awaitTermination()
