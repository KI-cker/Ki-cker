import tensorflow as tf
import keras.backend.tensorflow_backend as KTF

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
KTF.set_session(sess)

import seaborn as sns
from matplotlib import pyplot as plt

from keras.models import load_model
import sys
import numpy as np

def divide_and_round_up(a, b):
    c = a // b;
    if a > c * b:
        return c + 1
    else:
        return c

def plot_weights(weights, filename='model.jpg', number_of_columns=4):
    number_of_weights = len(weights)
    number_of_rows = divide_and_round_up(number_of_weights, number_of_columns)

    f, axes = plt.subplots(number_of_rows, number_of_columns)

    for k in range(number_of_rows):
        for j in range(number_of_columns):
            index = k * number_of_columns + j;

            if index < number_of_weights:
                sns.distplot(weights[index].flatten(), bins=50, ax = axes[k][j])
            else:
                axes[k][j].axis('off')

    f.set_size_inches(20, 10)
    f.set_tight_layout(True)

    plt.savefig(filename)
    plt.close()

def plot_layer(layer, filename='layer.jpg', number_of_columns=1, vmax=0.1):
    abs_layer = np.abs(np.array(layer))
    shape = abs_layer.shape

    input_channels = shape[2]
    output_channels = shape[3]

    number_of_rows = divide_and_round_up(output_channels, number_of_columns)

    f, axes = plt.subplots(number_of_rows * number_of_columns, input_channels)

    for k in range(number_of_rows):
        for j in range(number_of_columns):
            index = k * number_of_columns + j;

            print("layer {} {}".format(k, j))

            for l in range(input_channels):
                if index < output_channels:
                    sns.heatmap(abs_layer[:, :, l, index], ax=axes[index][l],
                            vmin=0, vmax=vmax,
                            cmap='Greens', 
                            cbar=False, xticklabels=False, yticklabels=False)
                else:
                    axes[k][j*input_channels + l].axis('off')

    f.set_size_inches(20, 40)
    f.set_tight_layout(True)

    plt.savefig(filename)
    plt.close()



    

filename = sys.argv[1]

print("Loading model {}".format(filename))

model = load_model(filename, custom_objects={'huber_loss': tf.losses.huber_loss})
weights = model.get_weights()

plot_weights(weights)
plot_layer(weights[0], vmax=0.1)

