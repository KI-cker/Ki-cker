import numpy as np

from kicker.train import DataProvider
from kicker import NeuralNet
from kicker.visualize import Figure

d = DataProvider(return_observations=True,
                 filename='train/training_data_new.h5')
s = d.get_batch()

nn = NeuralNet(23, (320, 480, 2))

fig = Figure()


def show_prediction(entry):
    prediction = nn.predict_single(entry['observation']).reshape(8, 3)
    print(np.argmax(prediction, axis=1) - np.ones(8))

    fig.plot(entry['observation'][:, :, 0], entry['observation']
             [:, :, 1], entry['observation_next'][:, :, 1], prediction)


for e in s:
    show_prediction(e)
