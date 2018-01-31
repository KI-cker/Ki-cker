import numpy as np
from datetime import datetime

from kicker.train import DataProvider
d = DataProvider()
s = d.get_batch()

from kicker.train import Trainer
from kicker import NeuralNet
nn = NeuralNet(24, (320, 480, 2))

t = Trainer(nn)

for j in range(1000):
    s = d.get_batch()
    _, loss, diff = t.train_step(s)
    print(datetime.utcnow(), j, 'Loss ', loss, ' diff ', diff)

nn.save()
