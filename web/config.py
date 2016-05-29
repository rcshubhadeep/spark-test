import os


def get_kafka_connection_string():
    host = os.getenv("KAFKA_HOST", "127.0.0.1")
    port = os.getenv("KAFKA_PORT", "9092")

    return host + ":" + port
