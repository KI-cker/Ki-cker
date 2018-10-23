import argparse

import random

import numpy as np
from datetime import datetime

from kicker.train import DataProvider, MemoryDataProvider
# d = DataProvider()

import tensorflow as tf
import keras.backend as K
from tensorflow.python.client import timeline


from kicker.train import Trainer
from kicker.neural_net import NeuralNet

import logging
logging.basicConfig(
    filename='train.log',
    level=logging.DEBUG,
    format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('-l','--learning_rate')
parser.add_argument('-g','--gamma')
args = parser.parse_args()

nn = NeuralNet()

t = Trainer(nn,gamma=args.gamma,learning_rate=args.learning_rate)

memory = MemoryDataProvider(filename='./Spieldaten/train.h5')
dataset = memory.load_as_dataset(max_number=5)

next_item = dataset.repeat().shuffle(1000).batch(32).prefetch(
    1).make_one_shot_iterator().get_next()

a, i, i_n, s, ter = next_item
step, loss, diff, computed, merged = t.compute(a, i, i_n, s, ter)

sess = K.get_session()
sess.run(tf.global_variables_initializer())

for j in range(5000):

    _, c_loss, c_diff, c_computed, c_merged = sess.run(
        [step, loss, diff, computed, merged])
    t.writer.add_run_metadata(t.run_metadata, "step%d" % j, j)
    t.writer.add_summary(c_merged, j)
    t.writer.flush()

    print(
        datetime.utcnow(),
        j,
        'Loss ',
        c_loss,
        ' diff ',
        np.mean(c_diff),
        ' computed moves ',
        np.sum(
            np.abs(
                c_computed -
                1)) /
        32 /
        8)


tl = timeline.Timeline(t.run_metadata.step_stats)
ctf = tl.generate_chrome_trace_format()
with open('timeline.json', 'w') as f:
    f.write(ctf)

nn.save()
