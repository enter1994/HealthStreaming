from kafka import KafkaProducer, KafkaConsumer

# import logging
from json import dumps, loads
import csv
import time

# logging.basicConfig(level=logging.INFO)

DATA_ROOT = './november_2021_COVID-19_Twitter_Streaming_Dataset.csv'
topic = 'Covid11'


producer=KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )



def make_producer(root, topic_name):
    with open(root, 'r') as f:
        reader = csv.reader(f)
        
        # head 지워줌
        next(reader)

        for message in reader:
            message = int(message[0])
            producer.send(topic_name, value=message)
            producer.flush()

    print('Done')



if __name__ == '__main__':
    make_producer(DATA_ROOT, topic)