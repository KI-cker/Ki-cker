import tensorflow as tf

from keras import backend as K


class Trainer:
    def __init__(self, neural_net, shape=(320, 480)):
        self.gamma = 0.9
        self.neural_net = neural_net

        self.width = shape[1]
        self.height = shape[0]

        self.tf_train_step = self.build_train_step()

    def build_train_step(self):
        inputs = tf.placeholder(tf.float32, shape=[None, self.height, self.width, 2], name='inputs')
        inputs_next = tf.placeholder(tf.float32, shape=[None, self.height, self.width, 2], name='inputs_next')

        rewards = tf.placeholder(tf.float32, shape=[None, 8], name='rewards')
        actions = tf.placeholder(tf.uint8, shape=[None, 8], name='actions')

        computed = self.evaluate_input(inputs)
        computed_next = self.evaluate_input(inputs_next)

        actions_one_hot = tf.one_hot(actions, 3, axis=2)

        q_old = tf.reduce_sum(actions_one_hot * computed, axis=2)


        second_term = self.gamma * tf.reduce_max(computed_next, axis=2)
        q_new = tf.stop_gradient(rewards + second_term)

        loss = tf.losses.huber_loss(q_new, q_old)

        train_step = tf.train.AdamOptimizer(1e-6).minimize(loss)

        return train_step, loss, tf.reduce_mean(tf.abs(q_new - q_old))

    def train_step(self, batch):
        sess = K.get_session()

        return sess.run(self.tf_train_step, feed_dict=self.build_feed_dict(batch))

    def evaluate_input(self, input):
        return tf.reshape(self.neural_net.model(input), [32, 8, 3])

    def build_feed_dict(self, batch):
        return {
            'rewards:0': [[s['score'],] * 8 for s in batch],
            'actions:0': [s['action'] for s in batch],
            'inputs:0': [s['observation'] for s in batch],
            'inputs_next:0': [s['observation_next'] for s in batch]
        }
