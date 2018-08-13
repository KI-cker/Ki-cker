import cv2
import numpy as np

from kicker.train import DataProvider, Parser
from kicker.neural_net import NeuralNet
from kicker.visualize import Figure

nn = NeuralNet(23, (320, 480, 5), filename='model.h5')

fig = Figure(wait_for_button_press=False, show_images=True, visualize_q_value=True)

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def plot_predictions(frames):
    observation = np.concatenate([(f[:, :, 1]).reshape((320, 480, 1)) for f in frames], axis=2)
    prediction = nn.predict_single(observation).reshape(8, 3)

    fig.plot(frames[1], frames[2], frames[3], prediction)


parser = Parser(filename='Spieldaten/hidden.h5')
interesting_games = ["game4", "game5", "game7", "game24", "game28", "game102", "game107", "game115", "game118",
                    "game133", "game149"]

for game_name in interesting_games:
    table_frames, positions, actions, scores = parser.get_game_data(game_name)

    length = len(table_frames)
    print("This is game: ", game_name)

    for j in range(4, length - 1):
        plot_predictions([table_frames[j + k] for k in range(-4, 1)])

    fig.figure.show()
