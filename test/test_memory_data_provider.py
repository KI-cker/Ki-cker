from kicker.train import MemoryDataProvider

import tensorflow as tf

m = MemoryDataProvider(filename='train/training_data.h5')


def test_memory_data_provder():
    data = m.get_train_game_data('game1')

    assert(len(data) > 10)

    item = data[0]

    assert(set(item.keys()) == {'action', 'score', 'images', 'images_next', 'terminal'})

def test_memory_data_provider_as_dataset():
    data = m.get_train_game_data_as_dataset('game1')

    shapes = data.output_shapes
    types = data.output_types

    assert(shapes[0].dims == [8])
    assert(shapes[1].dims == [320, 480, 5])
    assert(shapes[2].dims == [320, 480, 5])
    assert(shapes[3].dims == [8])
    assert(shapes[4].dims == [])

    assert(types[0] == tf.uint8)
    assert(types[1] == tf.float32)
    assert(types[2] == tf.float32)
    assert(types[3] == tf.float32)
    assert(types[4] == tf.bool)