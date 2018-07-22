import keras
import keras.backend as K
import tensorflow as tf
import uff

output_names = ['dense_2']
frozen_graph_filename = 'keras_vgg19_frozen_graph.pb'
sess = K.get_session()

from kicker.neural_net import NeuralNet

nn = NeuralNet()

# freeze graph and remove training nodes
graph_def = tf.graph_util.convert_variables_to_constants(
    sess, sess.graph_def, output_names)
graph_def = tf.graph_util.remove_training_nodes(graph_def)

# write frozen graph to file
with open(frozen_graph_filename, 'wb') as f:
    f.write(graph_def.SerializeToString())
    f.close()

    # convert frozen graph to uff
    uff_model = uff.from_tensorflow_frozen_model(
        frozen_graph_filename, output_names)
