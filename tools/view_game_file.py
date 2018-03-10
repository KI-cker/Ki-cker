import numpy as np

from kicker.train import DataProvider, Parser
from kicker.neural_net import NeuralNet
from kicker.visualize import Figure

# d = DataProvider(return_observations=True, filename='train/training_data_new.h5')
# s = d.get_batch()
#
nn = NeuralNet(23, (320, 480, 5), filename='/home/helge/tng/kicker/Ki-cker/model.h5')

fig = Figure(wait_for_button_press=False, show_images=True)

def show_prediction(frames):
    observation = np.concatenate([(f[:,:,1]).reshape((320, 480, 1)) for f in frames], axis=2)
    prediction = nn.predict_single(observation).reshape(8, 3)

    print(np.argmax(prediction, axis=1) - np.ones(8))

    fig.plot(frames[2], frames[3], frames[4], prediction)

parser = Parser(filename='train/Fabian_20180209_133730.h5')
# parser = Parser(filename='train/Fabian_20180308_080924.h5')

for game_name in parser.file:
    table_frames, positions, actions, scores = parser.get_game_data(game_name)

    length = len(table_frames)

    for j in range(1, length - 5):
        if scores[j] > 0.7:
            show_prediction([table_frames[j + k] for k in range(5)])
