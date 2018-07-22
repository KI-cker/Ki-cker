import numpy as np


def convert_neural_net_result_to_actions(inputs):
    inputs = np.array(inputs).reshape((8, 3))

    return (np.argmax(inputs, axis=1) - 1 * np.ones((8, ))).tolist()
