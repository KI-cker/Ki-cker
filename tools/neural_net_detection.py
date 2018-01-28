#!/usr/bin/env python

import tensorflow as tf
import h5py
import numpy as np
import argparse
import cv2


def ball_pos_and_scores_to_hdf5(games, PATH_TO_CKPT):

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    with detection_graph.as_default():
        config = tf.ConfigProto()
        config.gpu_options.allow_growth = True
        with tf.Session(graph=detection_graph, config=config) as sess:

            for game_name in games:
                print('Processing ', game_name)
                game = games[game_name]

                detected_pos = []
                ball_scores = []

                if 'ball_pos' in game:
                    del game['ball_pos']
                if 'ball_scores' in game:
                    del game['ball_scores']

                if 'table_frames' in game or 'table_frames_encoded' in game:
                    for frame_number in range(100):

                        if 'table_frames' in game:
                            frame = game['table_frames'][frame_number]
                        else:
                            encoded_frame = game['table_frames_encoded'][frame_number]
                            frame = cv2.imdecode(np.asarray(bytearray(encoded_frame)), 1)

                        # Definite input and output Tensors for detection_graph
                        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                        # Each box (y_min,x_min,y_max,x_max) represents a part of the image where a particular object was detected.
                        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                        # Each score represent how level of confidence for each of the objects.
                        # Score is shown on the result image, together with the class label.
                        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
                        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                        image_np_expanded = np.expand_dims(frame, axis=0)

                        (boxes, scores, classes, num) = sess.run(
                            [detection_boxes, detection_scores, detection_classes, num_detections],
                            feed_dict={image_tensor: image_np_expanded})

                        x_middle = int(round(0.5 * (boxes[0][0][1] * 480 + boxes[0][0][3] * 480)))
                        y_middle = int(round(0.5 * (boxes[0][0][0] * 320 + boxes[0][0][2] * 320)))

                        detected_pos.append(np.array([x_middle - 8, y_middle - 8]))
                        ball_scores.append(scores[0][0])

                    games.create_dataset(game_name + '/ball_pos', data=detected_pos)
                    games.create_dataset(game_name + '/ball_scores', data=ball_scores)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', help='HDF5 File the neural net shall detect the ball '
                                                   'and save the corresponding scores in')
    parser.add_argument('-f', '--frozen_interference_graph', help='Path to frozen inference graph')
    args = parser.parse_args()
    if args.input_file and args.frozen_interference_graph:
        games = h5py.File(args.input_file)
        ball_pos_and_scores_to_hdf5(games, args.frozen_interference_graph)
    else:
        print('Please specify a frozen interference graph and the HDF5 File where the ball shall be detected')


if __name__ == '__main__':
    main()
