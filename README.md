# Spark and Flask

## Assumptions:

1. It is running in a single machine. (To scale, dockerize the services and deploy via Kubernetes)

2. Everything is in the local host (You can specify a different Kafka host via environment vars KAFKA_HOST and KAFKA_PORT)

3. We use apache zookeeper, kafka, spark to achieve the goal.

4. The task is not complete. We are just outputting the aggregation in the console not storing it in a DB. We can use apache cassandra for an datastore at this layer and then write another spark batch job which will periodically offload this cassandra data to a mongodb (or any other data store)

5. The operating environment is Ubuntu 14.04

6. Why Flask? - Because it is easy to prototype something in it

7. Why Kafka? - Very high throughput and plays well with Spark

8. Why Python? - We could have used Go in the REST layer (and using goroutines to dispatch to the queue) but with PyKafka's async producer model Go does not buy anything extra. For the spark part I would like to say that there are only Python, Java, Scala and R officially supported with Spark.

9. Why proposing cassandra? - Very good for real time analytics. Enforces schema. We can easily use from pyspark using https://github.com/TargetHolding/pyspark-cassandra


## Preparations:

Before you can perform those steps, Please make sure that you have Oracle Java (OpenJDK does not play well with Spark), Python, python-pip and python-dev installed in the system.

1. Install spark in ubuntu - https://www.linkedin.com/pulse/getting-started-apache-spark-ubuntu-1404-myles-harrison

2. Install Zookeepr and Kafka - http://www.bogotobogo.com/Hadoop/BigData_hadoop_Zookeeper_Kafka.php

3. Clone this repo

4. Start Zookeeper and Kafka for the system to work (We assume that all the ports are default in this case.)

5. For the spark task you can configure the Zookeeper host and port via environment vars
ZOOKEEPER_HOST and ZOOKEEPER_PORT


## Start REST server:

Open a shell and go to web directory and use


```
python -u app.py
```

to start the server


## Start the spark job

go to the directory where you have installed spark and issue -


```
./bin/spark-submit --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.1 ~/spark-test/spark/test_wordcount.py
```

The last part of the comment should be replaced by the path where you have cloned the repo


## Fire events:

Now you are ready to fire events. Try using this -


```
curl -XPOST -d '{"event_type": "user_click", "timestamp": 123456789809, "params": {"key": "value"}}' http://put.server.ip.here:5000/api/events
```

## Watch the aggregation:

In the shell where you are running the spark task you can see the basic aggergation working


## Roardmap:

1. Persistent data via apache cassandra and later ETL the data in a cheaper store like S3 or mongo or anything

2. Docekerizing the services and deploying via kubernetes to easily scale them.

3. Finishing the app properly by smoothing all rough edges.

4. Create some install and run scripts to smooth the deploy process

5. Writing unit tests.
