import random

import numpy as np
from datetime import datetime

from kicker.train import DataProvider, MemoryDataProvider
# d = DataProvider()

from kicker.train import Trainer
from kicker.neural_net import NeuralNet
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


for j in range(5000):
    s = memory.get_batch()
    _, loss, diff, computed = t.train_step(s)

    print(datetime.utcnow(), j, 'Loss ', loss, ' diff ', np.mean(diff), ' computed moves ', np.sum(np.abs(computed - 1))/ 32 / 8, ' terminals ', np.sum([t['terminal'] for t in s]))


nn.save()
