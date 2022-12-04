import pandas as pd
import numpy as np
import datetime
import time
import random
from kafka import KafkaConsumer, KafkaProducer
from json import loads, dumps
from collections import Counter

import random
import hashlib
import sys

from CountMinSketch.countminsketch import *
# from hashfactory import hash_function

seed=0
np.random.seed(seed)
random.seed(seed)
sys.path.append('./CountMinSketch/')

_memomask = {}


def find_tweet_timestamp_post_snowflake(tid):
    offset = 1288834974657
    tstamp = (tid >> 22) + offset
    return tstamp

