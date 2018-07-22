import cv2
import h5py
import random
import numpy as np


class DataProvider:
    def __init__(self, filename='train/training_data.h5',
                 return_observations=False, frame_count=5):
        self.file = h5py.File(filename, 'r')
        self.games = [g for g in self.file if 'scores' in self.file[g]]
        self.shape = (320, 480)
        self.return_observations = return_observations
        self.frame_count = frame_count
        self.frame_range = range(-(self.frame_count - 1), 2)

    def get_batch(self, sample=32):
        return [self.get_single() for _ in range(sample)]

    def get_single(self):
        game_name = random.choice(self.games)
        game = self.file[game_name]

        index = random.choice(
            [k for k in game['good_indices'] if k > self.frame_count])
        if 'goals_received' in game:
            received_goal = index in game['goals_received']
        else:
            received_goal = []

        result = {
            'observations': [game['table_frames_encoded'][index + j] for j in self.frame_range],
            'score': 0.5 * game['scores'][index],
            'action': [a + 1 for a in game['actions'][index]],
            'terminal': received_goal
        }

        if received_goal:
            result['score'] = -100

        if self.return_observations:
            result['observation'] = self.build_input(game, index)
            result['observation_next'] = self.build_input(game, index + 1)

        return result

    def build_input(self, game, index):
        current = self.decode(game['table_frames_encoded'][index])
        next = self.decode(game['table_frames_encoded'][index + 1])

        return np.concatenate((current, next), axis=2)

    def decode(self, raw):
        b = bytearray()
        b.extend(raw)
        return cv2.imdecode(np.array(b), cv2.IMREAD_COLOR)[
            :, :, 1].reshape(self.shape + (1,))
