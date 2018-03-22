import logging

import numpy as np
import yaml
import random

from kicker.agents.agent import Agent
from kicker.agents.helper import convert_neural_net_result_to_actions
from kicker.image import Analyzer
from kicker.neural_net import NeuralNet

class NeuralNetAgent(Agent):
    def __init__(self, randomness=0.5, neural_net_filename='model.h5'):
        Agent.__init__(self)
        self.config = self.read_config()
        self.analyzer = Analyzer(self.config)
        self.input = None

        self.shape = (320, 480,  5)

        self.randomness = randomness

        self.neural_net = NeuralNet(24, self.shape, filename=neural_net_filename)

    def read_config(self):
        with open('config.yml', 'r') as f:
            return yaml.load(f)

    def new_frame(self, frame):
        frame = self.analyzer.extract_table(frame, (320, 480))[:, :, 1]
        first_frame = np.swapaxes(frame, 0, 1).reshape(320, 480, 1)
        if self.input is None:
            self.input = first_frame
            return
        self.input = np.concatenate((self.input, first_frame), axis=2)
        if self.input.shape[2] < 6:
            return
        self.input = self.input[:,:,1:]

        res = self.neural_net.predict_single(self.input)
        self.prediction = res
        self.inputs = convert_neural_net_result_to_actions(res)

        if random.random() < self.randomness:
            self.inputs = [random.randint(0, 2) - 1 for k in range(0, 8)]

        self.inputs_changed = True
        self.last_frame = first_frame

        return frame
