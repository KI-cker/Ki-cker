import random

import numpy as np

import h5py
import cv2
import yaml

class MemoryDataProvider:
    def __init__(self, filename='train/training_data.h5'):
        self.file = h5py.File(filename)
        self.frames = []

    def load(self):
        for game_name in self.file:
            self.frames = self.frames + self.get_train_game_data(game_name)

    def decode_image(self, raw):
        b = bytearray()
        b.extend(raw)
        return cv2.imdecode(np.array(b), cv2.IMREAD_COLOR)

    def get_train_game_data(self, game):
        data = self.file[game]
        table_frames = [self.decode_image(i)[:,:,1] for i in data['table_frames_encoded']]
        positions = [p for p in data['ball_pos']]
        actions = [a for a in data['actions']]
        scores = [s for s in data['scores']]
        goals_received = [s for s in data['goals_received']]
        good_indices = [i for i in data['good_indices']]

        length = len(table_frames)

        observations = [np.swapaxes(np.swapaxes(table_frames[k:k+6], 0, 2), 0, 1) for k in range(0, length - 7)]

        return [{
            'action': [a + 1 for a in actions[k + 5]],
            'score': scores[k + 5],
            'images': observations[k][:,:,:5],
            'images_next': observations[k][:,:,1:],
            'terminal': k + 5 in goals_received
        } for k in range(0, length - 7) if k + 5 in good_indices]

    def get_batch(self, sample=32):
        return random.sample(self.frames, sample)