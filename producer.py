from kafka import KafkaProducer

# import logging
from json import dumps, loads
import logging
import csv
# from count_min_sketch import *

DATA_ROOT = './november_2021_COVID-19_Twitter_Streaming_Dataset.csv'
TOPIC_NAME = 'Stream_CS_4'


producer=KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )


if __name__ == '__main__':

    print('Producing Data')

    with open('./november_2021_COVID-19_Twitter_Streaming_Dataset.csv', 'r') as f:
        reader = csv.reader(f)

        next(reader)

        print('Produce Data')
        for idx, message in enumerate(reader):

            message = int(message[0])
            producer.send(TOPIC_NAME, value=message)
            producer.flush()

            if idx == 50000:
                print('Data Index : ', idx)

    print('Produce Data Finish')