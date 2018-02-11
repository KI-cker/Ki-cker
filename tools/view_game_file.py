import numpy as np

from kicker.train import DataProvider, Parser
from kicker import NeuralNet
from kicker.visualize import Figure

# d = DataProvider(return_observations=True, filename='train/training_data_new.h5')
# s = d.get_batch()
#
nn = NeuralNet(23, (320, 480, 2))

fig = Figure()

def show_prediction(before, now, after):
    observation = np.concatenate((before[:,:,1].reshape((320, 480, 1)), now[:,:,1].reshape((320, 480, 1))), axis=2)
    prediction = nn.predict_single(observation).reshape(8, 3)

    print(np.argmax(prediction, axis=1) - np.ones(8))

    fig.plot(before, now, after, prediction)

parser = Parser(filename='train/Fabian_20180209_133730.h5')

for game_name in parser.file:
    table_frames, positions, actions, scores = parser.get_game_data(game_name)

    length = len(table_frames)

    for j in range(1, length - 1):
        show_prediction(table_frames[j-1], table_frames[j], table_frames[j+1])