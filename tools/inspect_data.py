from matplotlib import pyplot, cm
import numpy as np

from kicker.train import DataProvider
from kicker import NeuralNet

d = DataProvider(return_observations=True)
s = d.get_batch()

nn = NeuralNet(23, (320, 480, 2))

fig, axes = pyplot.subplots(1, 3)
fig.set_size_inches(18.5, 5)


def show_prediction(entry):
    prediction = nn.predict_single(entry['observation']).reshape(8, 3)
    axes[0].axis('off')
    axes[0].imshow(entry['observation'][:,:,0], cmap = cm.Greys_r)
    axes[1].axis('off')
    axes[1].imshow(entry['observation'][:,:,1], cmap = cm.Greys_r)
    axes[2].axis('off')
    axes[2].imshow(entry['observation_next'][:,:,1], cmap = cm.Greys_r)
    fig.tight_layout()

    # print(prediction)
    print(np.argmax(prediction, axis=1) - np.ones(8))
    fig.show()
    input('press enter')
    # pyplot.close()

for e in s:
    show_prediction(e)