import logging
import random

logger = logging.getLogger('Memory')

class BinnedData:
    def __init__(self):
        self.unseen_data = []

    def add_unseen_data(self, new_data):
        self.unseen_data = self.unseen_data + new_data

    def sample(self, batch_size=32):
        return random.sample(self.unseen_data, batch_size)
