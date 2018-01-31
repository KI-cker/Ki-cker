import numpy as np
from datetime import datetime

from kicker.train import DataProvider
d = DataProvider()
d2 = DataProvider('train/training_data_old.h5')

from kicker.train import Trainer
from kicker import NeuralNet
nn = NeuralNet(24, (320, 480, 2))

t = Trainer(nn)

for j in range(1000):
    s = d.get_batch(sample=16) + d2.get_batch(sample=16)
    _, loss, diff = t.train_step(s)
    print(datetime.utcnow(), j, 'Loss ', loss, ' diff ', diff)

nn.save()
