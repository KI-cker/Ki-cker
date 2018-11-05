import tensorflow as tf

from keras import backend as K

from kicker.neural_net import NeuralNet

from tensorflow.python import debug


class Trainer:
    def __init__(self, neural_net, shape=(320, 480), frame_count=5, gamma=0.99, learning_rate=1e-4):
        self.gamma = gamma
        self.punishment_for_moving = 0.1
        self.neural_net = neural_net
        self.neural_net_old = NeuralNet(filename=self.neural_net.filename)

        self.width = shape[0]
        self.height = shape[1]
        self.frame_count = frame_count

        self.options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
        self.run_metadata = tf.RunMetadata()

        self.writer = tf.summary.FileWriter(
            logdir='tensorboard_logdir', graph=K.get_session().graph)
        self.writer.flush()
        self.learning_rate = learning_rate

        self.observations_img = self.build_image_processor()

        self.debugger = False

    def build_image_processor(self):
        observations = tf.placeholder(
            tf.string, shape=[None, self.frame_count + 1], name='observations')
        observations_img = tf.cast(tf.map_fn(lambda i: self.convert_images(
            i), observations, dtype=tf.uint8), tf.float32)
        observations_img.set_shape(
            [None, self.width, self.height, self.frame_count + 1])

        return observations_img

    def compute(self, actions, inputs, inputs_next, rewards, terminals):
        computed = self.evaluate_input(inputs)
        computed_next = self.evaluate_input(inputs_next)
        computed_next_old = self.evaluate_input_old(inputs_next)
        # computed_actions = tf.stop_gradient(tf.argmax(computed, axis=2))
        actions_one_hot = tf.one_hot(actions, 3, axis=2)
        q_old = tf.reduce_sum(actions_one_hot * computed, axis=2)
        argmax_old = tf.one_hot(
            tf.argmax(
                computed_next_old,
                axis=2),
            3,
            axis=2)
        second_term = self.gamma * \
            tf.reduce_sum(computed_next * argmax_old, axis=2)
        # second_term = self.gamma * tf.reduce_max(computed_next, axis=2)
        q_new = tf.stop_gradient(
            rewards +
            tf.where(
                terminals,
                tf.zeros_like(second_term),
                second_term))

        loss = tf.losses.huber_loss(q_new, q_old, delta=50.0)
        # loss = loss + 0.01 * tf.reduce_mean(tf.where(computed_actions == tf.ones_like(computed_actions), tf.zeros_like(q_new), tf.ones_like(q_new)))
        # loss = loss + 0.1 * tf.reduce_mean(stf.nn.relu(computed[:,:,0] - computed[:,:,1]))
        # loss = loss + 0.1 * tf.reduce_mean(tf.nn.relu(computed[:,:,2] - computed[:,:,1]))
        with tf.name_scope('train'):
            train_step = tf.train.AdamOptimizer(
                self.learning_rate).minimize(loss)

        tf.summary.scalar('loss', loss)
        tf.summary.scalar('diff', tf.reduce_mean(tf.abs(q_new - q_old)))
        tf.summary.scalar('maximal_reward', tf.reduce_max(q_new))
        tf.summary.scalar('mean_reward', tf.reduce_mean(q_new))
        tf.summary.scalar('minimal_reward', tf.reduce_min(q_new))
        merged = tf.summary.merge_all()

        return train_step, loss, tf.abs(
            q_new - q_old), tf.argmax(computed, axis=2), merged

    def convert_images(self, inputs):
        return tf.transpose(tf.map_fn(lambda i: tf.image.decode_jpeg(
            i), inputs, dtype=tf.uint8)[:, :, :, 0], [1, 2, 0])

    def evaluate_input(self, input):
        return tf.reshape(self.neural_net.model(input), [32, 8, 3])

    def evaluate_input_old(self, input):
        return tf.reshape(self.neural_net_old.model(input), [32, 8, 3])
