import random

import numpy as np
from datetime import datetime

from kicker.train import DataProvider, MemoryDataProvider
# d = DataProvider()

import tensorflow as tf

from kicker.train import Trainer
from kicker.neural_net import NeuralNet

import logging
logging.basicConfig(filename='train.log', level=logging.DEBUG, format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s')


nn = NeuralNet()

t = Trainer(nn)

memory = MemoryDataProvider()
memory.load()


# memory = []


# def build_batch(provider, memory):
#     number_bad = min(int(len(memory) / 100), 0)
#     s = []
#     for _ in range(number_bad):
#         index = random.randint(0, len(memory) - 1)
#         s.append(memory[index])
#         del memory[index]
#
#     return number_bad, s + provider.get_batch(sample=32-number_bad)


for j in range(3000):
    s = memory.get_batch()
    _, loss, diff, computed, merged = t.train_step(s)
    t.writer.add_summary(merged, j)
    t.writer.add_run_metadata(tf.RunMetadata(), "step%d" % j)
    t.writer.flush()
    memory.update(diff)
    if j % 100 == 0:
        memory.data.log_statistics()

    print(datetime.utcnow(), j, 'Loss ', loss, ' diff ', np.mean(diff), ' computed moves ', np.sum(np.abs(computed - 1))/ 32 / 8, ' terminals ', np.sum([t['terminal'] for t in s]))


nn.save()
