import cv2
import h5py
import random
import numpy as np

class DataProvider:
    def __init__(self):
        self.file = h5py.File('train/training_data.h5', 'r')
        self.games = [g for g in self.file if 'scores' in self.file[g]]
        self.shape = (320, 480)

    def get_batch(self, sample=32):
        return [self.get_single() for _ in range(sample)]

    def get_single(self):
        game_name = random.choice(self.games)
        game = self.file[game_name]

        length = len(game['scores']) - 2

        index = random.randint(0, length)

        return {
            'observation': self.build_input(game, index),
            'observation_next': self.build_input(game, index + 1),
            'score': game['scores'][index],
            'action': [a + 1 for a in game['actions'][index]]
        }

    def build_input(self, game, index):
        current = self.decode(game['table_frames_encoded'][index])
        next = self.decode(game['table_frames_encoded'][index + 1])

        return np.concatenate((current, next), axis=2)

    def decode(self, raw):
        b = bytearray()
        b.extend(raw)
        return cv2.imdecode(np.array(b), cv2.IMREAD_COLOR)[:,:,1].reshape(self.shape + (1,))


