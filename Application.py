#!/usr/bin/env python
import cv2
import logging
import pygame
import numpy as np
from multiprocessing import Process, Queue
import sys, os
# import tensorflow as tf
import yaml

# from kicker.agents.neural_net_agent import NeuralNetAgent
from kicker.opcua_motor import MotorController

from kicker import ConsoleView, Helper
from kicker.agents import KeyboardAgent, RandomAgent
from kicker.storage import Storage, storage_worker
from kicker.image import add_ball, Analyzer

pygame.init()
pygame.font.init()

logging.basicConfig(filename='kicker.log', level=logging.DEBUG, format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s')
logging.info("Fussball ist wie Schach nur ohne Wuerfel")


# import keras.backend.tensorflow_backend as KTF

# def get_session(gpu_fraction=0.4):
#     num_threads = os.environ.get('OMP_NUM_THREADS')
#     gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_fraction)
# 
#     if num_threads:
#         return tf.Session(config=tf.ConfigProto(
#             gpu_options=gpu_options, intra_op_parallelism_threads=num_threads))
#     else:
#         return tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
# 
# 
# def set_keras_gpu_use(percentage):
#     KTF.set_session(get_session(gpu_fraction = percentage))
# 
# set_keras_gpu_use(0.4)

def read_config():
    with open('config.yml', 'r') as f:
        return yaml.load(f)

class Application(object):
    def __init__(self, agent, enable_storage=True):
        self.screen = None
        self.screen_width = 640
        self.screen_height = 480
        self.screen_width = 1024
        self.screen_height = 800
        self.view = ConsoleView()
        self.video = cv2.VideoCapture(1)
        self.inputs = [0, ] * 8
        self.agent = agent
        self.config = read_config()

        self.motor = MotorController()
        self.helper = Helper()

        self.enable_storage = enable_storage


        if self.enable_storage:
            self.storage_queue = Queue()
            self.storage_process = Process(target=storage_worker, args=(self.storage_queue, self.config))
            self.storage_process.start()

        self.analyzer = Analyzer(self.config)

    def submit_inputs(self):
        # cself.view.renderView(self.inputs)
        self.motor.control(self.inputs)

    def run(self):
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        while True:
            # logging.debug("Start event loop")
            if self.video.grab():
                r, f = self.video.retrieve()

                # self.possible_moves = self.analyzer.get_possible_moves(f)

                # img, c_x, c_y = add_ball(f[:])
                img = f[:]
                # img = self.analyzer.add_circles_to_limiters(img[:, :, ::-1])
                img = self.analyzer.extract_table(img, (self.screen_width, self.screen_height))

                # img = cv2.resize(img, (self.screen_width, self.screen_height))

                self.agent.new_frame(f)

                if self.enable_storage:
                    self.storage_queue.put((f, self.inputs))

                logging.debug("start updating window")
                pygame.surfarray.blit_array(self.screen, np.swapaxes(img[::, ::-1, :], 0, 1))
                # pygame.surfarray.blit_array(self.screen, img)
                pygame.display.update()
                # logging.debug("start processing events")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # stop_all()
                    if self.enable_storage:
                        self.storage_queue.put((None, None))
                        self.storage_process.join()

		    self.motor.disconnect()
                    pygame.quit()
                    sys.exit()

                self.agent.handle_event(event)

            inputs = self.agent.get_inputs()

            if inputs is not None:
                # self.inputs = self.helper.handle_forbidden_moves(self.possible_moves, inputs)
                self.inputs = inputs
                self.submit_inputs()

if __name__ == '__main__':
    agent = RandomAgent()
    # agent = KeyboardAgent()
    # agent = NeuralNetAgent()
    program = Application(agent, enable_storage=False)
    program.run()
