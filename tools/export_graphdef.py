import keras
import keras.backend as K
import tensorflow as tf

import uff

from kicker.neural_net import NeuralNet

output_names = ['dense_2/BiasAdd']
frozen_graph_filename = 'frozen_model.pb'

nn = NeuralNet()

sess = K.get_session()
tf.summary.FileWriter('tensorboard_logdir', sess.graph)

graph_def = tf.graph_util.convert_variables_to_constants(sess, sess.graph_def, output_names)

graph_def = tf.graph_util.remove_training_nodes(graph_def)

# write frozen graph to file
with open(frozen_graph_filename, 'wb') as f:
    f.write(graph_def.SerializeToString())
    f.close()

# convert frozen graph to uff
uff.from_tensorflow_frozen_model(frozen_graph_filename, output_names, output_filename='model.uff')


