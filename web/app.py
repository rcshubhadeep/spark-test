from flask import Flask, request
from flask_restful import Resource, Api
from pykafka import KafkaClient

from config import get_kafka_connection_string

import json

app = Flask(__name__)
api = Api(app)


def connect_to_kafka():
    connection_string = get_kafka_connection_string()
    client = KafkaClient(hosts=connection_string)
    return client


kafka_client = connect_to_kafka()
topic = client.topics['MyTopic']


class MessagePost(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        with topic.get_producer() as producer:
            producer.produce(json.dumps(json_data))

api.add_resource(MessagePost, '/api/events')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
