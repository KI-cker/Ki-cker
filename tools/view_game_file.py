import cv2
import numpy as np
import time
import json
import base64

from kicker.train import DataProvider, Parser
from kicker.neural_net import NeuralNet
from kicker.visualize import Figure

# d = DataProvider(return_observations=True, filename='train/training_data_new.h5')
# s = d.get_batch()
#
nn = NeuralNet(23, (320, 480, 5), filename='model.h5')

fig = Figure(wait_for_button_press=False, show_images=True)

import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def show_prediction(frames, position):
    observation = np.concatenate(
        [(f[:, :, 1]).reshape((320, 480, 1)) for f in frames], axis=2)
    prediction = nn.predict_single(observation).reshape(8, 3)

    print(
        np.argmax(
            prediction,
            axis=1) -
        np.ones(8),
        position,
        np.min(prediction))

    # ball_frame = frames[4].copy()
    # cv2.circle(ball_frame, tuple(position + 9), 9, (255, 0, 0))
    #
    # fig.plot(frames[2], frames[3], ball_frame, prediction)
    img_enc = cv2.imencode('.jpg', frames[4])[1].tostring().encode('base64')
    sock.sendto(img_enc, ('localhost', 1882))
    sock.sendto(
        json.dumps(
            np.max(
                prediction,
                axis=1).tolist()).encode(),
        ('localhost',
         1881))


# parser = Parser(filename='train/Fabian_20180209_095009.h5')
# parser = Parser(filename='train/Fabian_20180209_133730.h5')
# parser = Parser(filename='train/Fabian_20180308_080924.h5')
parser = Parser(filename='train/Fabian_20180314_133913.h5')
# parser = Parser(filename='train/Fabian_20180314_091655.h5')

for game_name in parser.file:
    table_frames, positions, actions, scores = parser.get_game_data(game_name)

    length = len(table_frames)

    for j in range(4, length - 1):
        # if scores[j] > 0.7:
        show_prediction([table_frames[j + k]
                         for k in range(-4, 1)], positions[j])
