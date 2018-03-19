import tensorflow as tf

from keras import backend as K

from kicker.neural_net import NeuralNet


class Trainer:
    def __init__(self, neural_net, shape=(320, 480), frame_count=5):
        self.gamma = 0.99
        self.punishment_for_moving = 0.1
        self.neural_net = neural_net
        self.neural_net_old = NeuralNet(filename=self.neural_net.filename)

        self.width = shape[0]
        self.height = shape[1]
        self.frame_count = frame_count

        self.observations_img = self.build_image_processor()
        self.tf_train_step = self.build_train_step()

        # writer = tf.summary.FileWriter(logdir='logs', graph=K.get_session.get_graph())
        # writer.flush()


    def build_image_processor(self):
        observations = tf.placeholder(tf.string, shape=[None, self.frame_count + 1], name='observations')
        observations_img = tf.cast(tf.map_fn(lambda i: self.convert_images(i), observations, dtype=tf.uint8), tf.float32)
        observations_img.set_shape([None, self.width, self.height, self.frame_count + 1])

        return observations_img

    def decode(self, images):
        sess = K.get_session()

        return sess.run(self.observations_img, feed_dict={
            'observations:0': images
        })

    def build_train_step(self):
        rewards = tf.placeholder(tf.float32, shape=[None, 8], name='rewards')
        actions = tf.placeholder(tf.uint8, shape=[None, 8], name='actions')
        terminals = tf.placeholder(tf.bool, shape=[None], name='terminal')


        # inputs = self.observations_img[:,:,:,:self.frame_count]
        # inputs_next = self.observations_img[:,:,:,1:]

        # inputs.set_shape([None, self.width, self.height, self.frame_count])
        # inputs_next.set_shape([None, self.width, self.height, self.frame_count])

        inputs = tf.placeholder(tf.float32, shape=[None, self.width, self.height, self.frame_count], name='inputs')
        inputs_next = tf.placeholder(tf.float32, shape=[None, self.width, self.height, self.frame_count], name='inputs_next')


        computed = self.evaluate_input(inputs)
        computed_next = self.evaluate_input(inputs_next)
        computed_next_old = self.evaluate_input_old(inputs_next)
        computed_actions = tf.stop_gradient(tf.argmax(computed, axis=2))

        actions_one_hot = tf.one_hot(actions, 3, axis=2)

        q_old = tf.reduce_sum(actions_one_hot * computed, axis=2)

        argmax_old = tf.one_hot(tf.argmax(computed_next_old, axis=2), 3, axis=2)
        second_term = self.gamma * tf.reduce_sum(computed_next * argmax_old, axis=2)
        q_new = tf.stop_gradient(rewards + tf.where(terminals, tf.zeros_like(second_term), second_term))

        loss = tf.losses.huber_loss(q_new, q_old)
        # loss = loss + 0.01 * tf.reduce_mean(tf.where(computed_actions == tf.ones_like(computed_actions), tf.zeros_like(q_new), tf.ones_like(q_new)))
        # loss = loss + 0.1 * tf.reduce_mean(tf.nn.relu(computed[:,:,0] - computed[:,:,1]))
        # loss = loss + 0.1 * tf.reduce_mean(tf.nn.relu(computed[:,:,2] - computed[:,:,1]))

        train_step = tf.train.AdamOptimizer(1e-5).minimize(loss)

        return train_step, loss, tf.abs(q_new - q_old), tf.argmax(computed, axis=2)

    def convert_images(self, inputs):
        return tf.transpose(tf.map_fn(lambda i: tf.image.decode_jpeg(i), inputs, dtype=tf.uint8)[:,:,:,0], [1,2,0])


    def train_step(self, batch):
        sess = K.get_session()

        return sess.run(self.tf_train_step, feed_dict=self.build_feed_dict(batch))

    def evaluate_input(self, input):
        return tf.reshape(self.neural_net.model(input), [32, 8, 3])

    def build_feed_dict(self, batch):
        return {
            'rewards:0': [[s['score'],] * 8 for s in batch],
            'actions:0': [s['action'] for s in batch],
            # 'observations:0': [s['observations'] for s in batch],
            'terminal:0': [s['terminal'] for s in batch],
            'inputs:0': [s['images'] for s in batch],
            'inputs_next:0': [s['images_next'] for s in batch]
        }

    def evaluate_input_old(self, input):
        return tf.reshape(self.neural_net_old.model(input), [32, 8, 3])
