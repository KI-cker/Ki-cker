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


nn = NeuralNet()

t = Trainer(nn)

memory = MemoryDataProvider()
memory.load()

dataset = memory.get_as_dataset()
next_item = dataset.repeat().batch(32).prefetch(
    1).make_one_shot_iterator().get_next()


sess = K.get_session()

a, i, i_n, s, ter = next_item
step, loss, diff, computed, merged = t.compute(a, i, i_n, s, ter)

sess.run(tf.initialize_all_variables())

for j in range(5000):

    t.writer.add_run_metadata(t.run_metadata, "step%d" % j, j)
    t.writer.add_summary(c_merged, j)
    t.writer.flush()
    _, c_loss, c_diff, c_computed, c_merged = sess.run(
        [step, loss, diff, computed, merged])
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
