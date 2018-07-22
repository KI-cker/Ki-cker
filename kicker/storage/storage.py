import cv2
import h5py
import numpy as np
import logging

import time
import yaml


class Storage():
    def __init__(self, config, filename='games.h5'):
        self.file = h5py.File(filename, 'a')
        self.frames = None
        self.actions = None
        self.shape = None
        self.times = None
        self.config = config

    def add_frame(self, frame):
        if self.frames is None:
            self.shape = (1, ) + frame.shape
            self.frames = [cv2.imencode('.jpg', frame)[1].tostring()]
            # self.frames = frame.reshape(self.shape)
            self.times = [time.time()]
        else:
            self.frames.append(cv2.imencode('.jpg', frame)[1].tostring())
            self.times.append(time.time())
            # self.frames = np.concatenate((self.frames, frame.reshape(self.shape)), axis=0)

    def add_action(self, action):
        action = np.array(action)
        if self.actions is None:
            self.actions = action.reshape((1, 8))
        else:
            self.actions = np.concatenate(
                (self.actions, action.reshape(1, 8)), axis=0)

    def save(self):
        dataset_name = self._next_dataset()
        logging.info("Saving to dataset %s", dataset_name)
        g = self.file.create_group(self._next_dataset())
        g.attrs['config'] = yaml.dump(self.config)
        g.create_dataset('frames', data=self.frames, compression='lzf')
        g.create_dataset('actions', data=self.actions, compression='lzf')
        g.create_dataset('times', data=self.times, compression='lzf')
        self.file.flush()
        self._reset()
        logging.info("Done saving")

    def _reset(self):
        self.frames = None
        self.actions = None
        self.times = None

    def _next_dataset(self):
        return "game{}".format(len(self.file.keys()) + 1)
