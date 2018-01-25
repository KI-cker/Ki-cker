import random

from kicker.agents.agent import Agent


class RandomAgent(Agent):
    def __init__(self):
        Agent.__init__(self)

    def new_frame(self, frame):
        self.inputs = [random.randint(0, 2) - 1 for k in range(0, 8)]
        self.inputs_changed = True
