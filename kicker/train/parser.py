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

        b = bytearray()
        b.extend(raw)

        return cv2.imdecode(np.array(b), cv2.IMREAD_COLOR)

    def get_config(self, game):
        raw = self.file[game].attrs['config']
        return yaml.load(raw)