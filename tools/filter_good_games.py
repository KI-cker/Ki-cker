import h5py
import cv2

from kicker.train import Parser


p = Parser('train/games.h5')
f = h5py.File('train/training_data.h5')


def encode_frames(frames):
    return [cv2.imencode('.jpg', f)[1].tostring() for f in frames]


def add_new_group_to_file(f, frames, positions, actions):
    current_count = len(f)
    new_name = "game{}".format(current_count + 1)

    group = f.create_group(new_name)
    group['table_frames_encoded'] = encode_frames(frames)
    group['actions'] = actions
    group['ball_pos'] = positions


for g in p.file:
    print("Processing {}".format(g))
    frames, positions, actions = p.get_game_data(g)
    vals_x = len(set([p[0] for p in positions]))
    vals_y = len(set([p[1] for p in positions]))
    if vals_x > 20 or vals_y > 20:
        add_new_group_to_file(f, frames, positions, actions)