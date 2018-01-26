import numpy as np

import h5py
import cv2

class Parser:
    def __init__(self, filename):
        self.file = h5py.File(filename)

    def get_frame(self, game, id):
        raw = self.file[game]['frames'][id]

        b = bytearray()
        b.extend(raw)

        return cv2.imdecode(np.array(b), cv2.IMREAD_COLOR)
