import argparse
import sys
import requests
import os
import json
from kafka import KafkaProducer

def main(config_path):
    with open(config_path) as f:
        topic = json.load(f)['topic']

    producer = KafkaProducer(
        bootstrap_servers=[os.getenv('KAFKA_BROKER')],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    params = {"feed": "kontur-public", "eventType": topic.upper()}
    headers = {"Authorization": f"Bearer {os.getenv('KONTUR_ACCESS_TOKEN')}"}
    response = requests.get("https://apps.kontur.io/events/v1", params=params, headers=headers)

    for event in response.json()["events"]:
        producer.send(topic, value=event)

if __name__ == "__main__":
    main(sys.argv[1])