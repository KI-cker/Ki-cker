import cv2
import pygame
import numpy as np
import h5py
import sys
import os
import yaml

def load_frame():
    f = h5py.File('games.h5')
    g = f['game1']
    frames = g['frames']
    return frames[0]

def get_frame_camera():
    cap = cv2.VideoCapture(1)
    r, f = cap.read()
    return f

def get_variable_name():
    if len(sys.argv) < 2:
        print("Please specify a variable name to be set")
        sys.exit()

    var_name = sys.argv[1]
    print("Setting {}".format(var_name))
    return var_name

def set_variable(var_name, value):
    config = {}
    config_file_name = 'config.yml'
    if os.path.exists(config_file_name):
        with open(config_file_name, 'r') as f:
            config = yaml.load(f)

    if not config.has_key('coordinates'):
        config['coordinates'] = {};

    config['coordinates'][var_name] = value

    with open(config_file_name, 'w') as f:
        f.write(yaml.dump(config))


def terminate():
    pygame.quit()
    sys.exit()

def main():
    var_name = get_variable_name()
    pygame.init()

    # frame = load_frame()
    frame = get_frame_camera()
    shape = frame.shape
    screen = pygame.display.set_mode((shape[0], shape[1]))

    pygame.surfarray.blit_array(screen, frame)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONUP:
                set_variable(var_name, [event.pos[1], event.pos[0]])
                terminate()

if __name__ == '__main__':
    main()
