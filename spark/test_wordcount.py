from pyspark.sql import SQLContext
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import json
import os


def get_zookerper_connect_string():
    host = os.getenv("ZOOKEEPER_HOST", "localhost")
    port = os.getenv("ZOOKEEPER_PORT", "2181")
    return host + ":" + port


sc = SparkContext()
sql = SQLContext(sc)
stream = StreamingContext(sc, 1)  # 1 second window

kafka_stream = KafkaUtils.createStream(stream,
                                       get_zookerper_connect_string(),
                                       'event_streaming_consumer',
                                       {"MyTopic": 1})


def analyze(grouping):
    if 'event_type' not in grouping:
        return (None, None)

    return (grouping['event_type'], grouping)


parsed = kafka_stream.map(lambda (k, v): json.loads(v))

red = parsed.map(analyze)
red.pprint()

stream.start()
stream.awaitTermination()
