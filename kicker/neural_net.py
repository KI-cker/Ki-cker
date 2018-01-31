import os

from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Conv2D
from keras.layers.convolutional import Convolution2D
from keras import backend as K

def build_net(input_shape, num_outputs):
    model = Sequential()
    model.add(Conv2D(32, (11, 11), padding='same', strides=(5, 5), activation='relu', input_shape=input_shape))
    model.add(Conv2D(64, (4, 4), padding='same', strides=(2, 2), activation='relu'))
    model.add(Conv2D(64, (3, 3), padding='same', strides=(2, 2), activation='relu'))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dense(24))

    model.compile(loss='mse', optimizer='adam')

    return model

class NeuralNet():
    def __init__(self, num_output, input_shape, filename='model.h5'):
        self.num_output = num_output
        self.input_shape = input_shape
        self.filename = filename
        if os.path.isfile(self.filename):
            self.model = load_model(self.filename)
        else:
            self.model = build_net(input_shape, num_output)

    def save(self):
        self.model.save(self.filename)

    def predict(self, frames):
        prediction = self.model.predict(frames)
        return prediction

    def predict_single(self, frame):
        return self.predict(frame.reshape((-1,) + self.input_shape))

    def train(self, inputs, targets):
        self.model.fit(inputs, targets, nb_epoch=1)
