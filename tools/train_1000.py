import random

import numpy as np
from datetime import datetime

from kicker.train import DataProvider
d = DataProvider()

from kicker.train import Trainer
from kicker import NeuralNet
nn = NeuralNet(24, (320, 480, 2))

t = Trainer(nn)




memory = []


def build_batch(provider, memory):
    number_bad = min(int(len(memory) / 100), 5)
    s = []
    for _ in range(number_bad):
        index = random.randint(0, len(memory) - 1)
        s.append(memory[index])
        del memory[index]

    return number_bad, s + provider.get_batch(sample=32-number_bad)


for j in range(1000):
    number_bad, s = build_batch(d, memory)
    _, loss, diff = t.train_step(s)

    bad_indices = np.where(diff > 5)[0]
    for k in bad_indices:
        if k > number_bad:
             memory.append(s[int(k)])

    print(datetime.utcnow(), j, 'Loss ', loss, ' diff ', np.mean(diff), ' large ', len(bad_indices), ' memory ', len(memory))


nn.save()
