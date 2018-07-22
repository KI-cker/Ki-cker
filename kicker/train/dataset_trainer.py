import tensorflow as tf

from kicker.neural_net import NeuralNet


class DatasetTrainer:
    def __init__(self, neural_net, generator, shape=(320, 480), frame_count=5):
        self.gamma = 0.99
        self.punishment_for_moving = 0.1
        self.neural_net = neural_net
        self.neural_net_old = NeuralNet(filename=self.neural_net.filename)

        self.width = shape[0]
        self.height = shape[1]
        self.frame_count = frame_count

        self.dataset = tf.data.Dataset.from_generator(
            generator, (tf.int32, tf.bool, tf.float32, tf.float32, tf.float32))

        self.dataset = self.dataset.repeat().shuffle(buffer_size=1000).batch(32)

        actions, terminals, rewards, inputs, inputs_next = self.dataset.make_one_shot_iterator().get_next()

        computed = self.evaluate_input(inputs)
        computed_next = self.evaluate_input(inputs_next)
        computed_next_old = self.evaluate_input_old(inputs_next)

        actions_one_hot = tf.one_hot(actions, 3, axis=2)

        q_old = tf.reduce_sum(actions_one_hot * computed, axis=2)

        argmax_old = tf.one_hot(
            tf.argmax(computed_next_old, axis=2), 3, axis=2)
        second_term = self.gamma * \
            tf.reduce_sum(computed_next * argmax_old, axis=2)
        q_new = tf.stop_gradient(
            rewards + tf.where(terminals, tf.zeros_like(second_term), second_term))

        loss = tf.losses.huber_loss(q_new, q_old)

        self.train_step = tf.train.AdamOptimizer(1e-5).minimize(loss)

    def evaluate_input(self, input):
        return tf.reshape(self.neural_net.model(input), [32, 8, 3])

    def evaluate_input_old(self, input):
        return tf.reshape(self.neural_net.model(input), [32, 8, 3])
