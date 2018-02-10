import argparse

import h5py
import cv2
import numpy as np

from kicker.train import Parser


def encode_frames(frames):
    return [cv2.imencode('.jpg', f)[1].tostring() for f in frames]

def add_new_group_to_file(f, frames, positions, actions, good_indices):
    current_count = len(f)
    new_name = "game{}".format(current_count + 1)

    print('Adding {}'.format(new_name))

    group = f.create_group(new_name)
    group['table_frames_encoded'] = encode_frames(frames)
    group['actions'] = actions
    group['ball_pos'] = positions
    group['good_indices'] = good_indices

def process(p, f):
    for g in p.file:
        print("Processing {}".format(g))
        frames, positions, actions, scores = p.get_game_data(g)
        scores = np.array(scores)
        number = len(scores)
        good_indices = [index for index in range(1, number) if np.min(scores[index-1:index+2]) > 0.9]

        if len(good_indices) > 5:
            add_new_group_to_file(f, frames, positions, actions, good_indices)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file')
    parser.add_argument('-o', '--output_file')
    args = parser.parse_args()
    if args.input_file and args.output_file:
        p = Parser(args.input_file)
        f = h5py.File(args.output_file)
        process(p, f)


if __name__ == '__main__':
    main()