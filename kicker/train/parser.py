import numpy as np

import h5py
import cv2
import yaml

class Parser:
    def __init__(self, filename):
        self.file = h5py.File(filename)

    def get_number_of_frames(self, game):
        return len(self.file[game]['frames'])

    def get_frame(self, game, id):
        raw = self.file[game]['frames'][id]

        return self.decode_image(raw)

    def decode_image(self, raw):
        b = bytearray()
        b.extend(raw)
        return cv2.imdecode(np.array(b), cv2.IMREAD_COLOR)

    def get_config(self, game):
        raw = self.file[game].attrs['config']
        return yaml.load(raw)

    def get_game_data(self, game):
        data = self.file[game]
        table_frames = [self.decode_image(i) for i in data['table_frames_encoded']]
        positions = [p for p in data['ball_pos']]
        actions = [a for a in data['actions']]
        scores = [s for s in data['ball_scores']]

        return table_frames, positions, actions, scoress

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
            'action': actions[k + 5],
            'score': scores[k + 5],
            'images': observations[k],
            'terminal': k + 5 in goals_received
        } for k in range(0, length - 7) if k + 5 in good_indices]

