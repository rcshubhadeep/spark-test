from flask import Flask, request
from flask_restful import Resource, Api
from pykafka import KafkaClient

from config import get_kafka_connection_string

import json
import sys

app = Flask(__name__)
api = Api(app)


def connect_to_kafka():
    connection_string = get_kafka_connection_string()
    client = KafkaClient(hosts=connection_string)
    return client

try:
    kafka_client = connect_to_kafka()
    topic = kafka_client.topics['MyTopic']
    producer = topic.get_producer()
except:
    sys.exit(1)


class MessagePost(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        producer.produce(json.dumps(json_data))
        return "", 201

api.add_resource(MessagePost, '/api/events')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
