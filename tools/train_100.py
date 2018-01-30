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
    print(j, 'Loss ', loss, ' diff ', np.mean(np.max(diff, axis=1)))

nn.save()