from kafka import KafkaConsumer
import sys
import boto3
import os
import json
from datetime import datetime

def main(config_path):
    with open(config_path) as f:
        topic = json.load(f)['topic']

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[os.getenv('KAFKA_BROKER')],
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    s3 = boto3.client('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )

    for message in consumer:
        s3.put_object(
            Bucket="bronze",
            Key=f"gdacs/{topic}/{datetime.now()}.json",
            Body=json.dumps(message.value)
        )

if __name__ == "__main__":
    main(sys.argv[1])