from kafka import KafkaConsumer

import json
import logging
from json import dumps, loads
from collections import Counter
import csv
import datetime
import time

from CountMinSketch.countminsketch import *
from CountMinSketch.hashfactory import *



def find_tweet_timestamp_post_snowflake(tid):
    offset = 1288834974657
    tstamp = (tid >> 22) + offset
    return tstamp


TOPIC_NAME = 'Stream_CS_1'
DEPTH = 5
WIDTH = 7
HASH_FUNCTIONS = [hash_function(i) for i in range(DEPTH)]
batch = Counter()
sketch = CountMinSketch(DEPTH, WIDTH, HASH_FUNCTIONS)
# COUNT = 9*(10**7)

WEEKDAY = {'Mon':0,
           'Tue':1,
           'Wed':2,
           'Thu':3,
           'Fri':4,
           'Sat':5,
           'Sun':6
          }


# produce random hashmap
hash_map = []
for i in range(len(HASH_FUNCTIONS)):
    list_=[]
    for j in range((WIDTH)):
        list_.append(HASH_FUNCTIONS[i](j)%WIDTH)
        # print(HASH_FUNCTIONS[i](j)%WIDTH, end=' ')
    hash_map.append(list_)
hash_map =np.array(hash_map)

if __name__ == '__main__':

    consumer=KafkaConsumer(TOPIC_NAME,
                        bootstrap_servers=['localhost:9092'],
                        auto_offset_reset="earliest",
                        enable_auto_commit=True,
                        # group_id='my-group',
                        value_deserializer=lambda x: loads(x.decode('utf-8')),
                        consumer_timeout_ms=1000
        )


    print('Consuming Data')

    while True:
        for message in consumer:
            message_t = message.topic
            message_p = message.partition
            message_o = message.offset
            message_k = message.key
            message_v = message.value

            if message_o % 10000 == 0:
                print('Data Index : ', message_o)

            timestamp = find_tweet_timestamp_post_snowflake(message_v)
            current_date = datetime.datetime.fromtimestamp(timestamp/1000)

            hour = current_date.hour
            weekday = WEEKDAY[current_date.ctime().split()[0]]

            batch[weekday]+=1

            for key, count in batch.items():
                sketch.add(key, count)

            batch.clear()
            frequency = []

            # Monday to Sunday
            for index in range(WIDTH):
                freq = min([sketch.get_matrix()[i][j] for i,j in enumerate([j for j in hash_map[:, index]])])
                frequency.append(int(freq))

            with open(f'./weekday_count.json', 'w') as f:
                json.dump(frequency, f)

        consumer.close()
        