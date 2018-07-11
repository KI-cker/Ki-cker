import random

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
        games = [g for g in self.file]
        for game_name in random.sample(games, 5):
        # min(200, len(games))):
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
        actions = [a for a in data['actions']]
        scores = [0.01 * s for s in data['scores']]
        goals_received = [s for s in data['goals_received']]
        good_indices = [i for i in data['good_indices']]

        length = len(table_frames)

        observations = [np.swapaxes(np.swapaxes(table_frames[k-4:k+1], 0, 2), 0, 1) for k in range(5, length)]

        for k in goals_received:
            scores[k] = - 100

        data = []
        for k in range(0, len(observations) - 5):
            if k in good_indices:
                step = random.randint(1, 5)
                terminal = False
                for l in range(0, step):
                    if k + l in goals_received:
                        step = l
                        terminal = True
                        break

                score = np.sum([0.99 ** l * scores[k + l] for l in range(0, step + 1)])

                data.append({
                    'action': [a + 1 for a in actions[k]],
                    'score': score,
                    'images': observations[k],
                    'images_next': observations[k + step],
                    'terminal': terminal
                })

        return data

    def generator(self):
        for d in self.data.unseen_data:
            yield(d['action'], d['terminal'], [d['score'],]*8, d['images'], d['images_next'])

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
        self.data.update_with_deltas(np.max(diff, axis=1))

    def get_as_dataset(self):
        def get_slice_for_key(key, type=np.float32):
            return np.array([d[key] for d in self.data.unseen_data], dtype=type)

        return tf.data.Dataset.from_tensor_slices((
            get_slice_for_key('action', np.uint8),
            get_slice_for_key('images'),
            get_slice_for_key('images_next'),
            np.array([[d['score'], ] * 8 for d in self.data.unseen_data], dtype=np.float32),
            get_slice_for_key('terminal', np.bool)))
