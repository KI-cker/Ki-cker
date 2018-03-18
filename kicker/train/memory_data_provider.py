import tensorflow as tf

from keras import backend as K


import numpy as np

import h5py
import cv2

from kicker.train import BinnedData


class MemoryDataProvider:
    def __init__(self, filename='train/training_data.h5'):
        self.file = h5py.File(filename)
        self.width = 320
        self.height = 480
        self.frames = []

        self.data = BinnedData()

        self.observations_img = self.build_decoder()

    def load(self):
        for game_name in self.file:
            self.data.add_unseen_data(self.get_train_game_data(game_name))
            print('Done loading {}', game_name)

    def decode_image(self, raw):
        b = bytearray()
        b.extend(raw)
        return cv2.imdecode(np.array(b), cv2.IMREAD_COLOR)

    def get_train_game_data(self, game):
        data = self.file[game]

        images = self.decode([i for i in data['table_frames_encoded']])

        table_frames = [i[:,:,1] for i in images]
        positions = [p for p in data['ball_pos']]
        actions = [a for a in data['actions']]
        scores = [s for s in data['scores']]
        goals_received = [s for s in data['goals_received']]
        good_indices = [i for i in data['good_indices']]

        length = len(table_frames)

        observations = [np.swapaxes(np.swapaxes(table_frames[k:k+6], 0, 2), 0, 1) for k in range(0, length - 7)]

        for k in goals_received:
            scores[k] = - 100

        return [{
            'action': [a + 1 for a in actions[k + 5]],
            'score': scores[k + 5],
            'images': observations[k][:,:,:5],
            'images_next': observations[k][:,:,1:],
            'terminal': k + 5 in goals_received
        } for k in range(0, length - 7) if k + 5 in good_indices]

    def get_batch(self, sample=32):
        return self.data.sample(sample)

    def build_decoder(self):
        observations = tf.placeholder(tf.string, shape=[None], name='observations_conv')
        observations_img = tf.cast(tf.map_fn(lambda i: tf.image.decode_jpeg(i), observations, dtype=tf.uint8), tf.float32)
        observations_img.set_shape([None, self.width, self.height, 3])

        return observations_img

    def decode(self, images):
        sess = K.get_session()

        return sess.run(self.observations_img, feed_dict={
            'observations_conv:0': images
        })

    def update(self, diff):
        pass
