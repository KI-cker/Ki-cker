import logging
import time

import cv2
import yaml
from multiprocessing import Queue, Process

from kicker.opcua_motor import MotorController
from kicker.storage import storage_worker

def worker(queue, name, model, randomness):
    import tensorflow as tf
    from kicker.agents.neural_net_agent import NeuralNetAgent
    import keras.backend.tensorflow_backend as KTF

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    KTF.set_session(sess)

    import pygame
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((1024, 800))

    logging.info('started session')

    agent = NeuralNetAgent(randomness=randomness, neural_net_filename=model)

    logging.info('started neural net')
    motor = MotorController()

    motor.resetEmulation()

    logging.info('started motor')

    video = cv2.VideoCapture(1)

    logging.info('started video')

    with open('config.yml', 'r') as f:
        yaml_config = yaml.load(f)

    storage_queue = Queue()
    storage_process = Process(target=storage_worker, args=(storage_queue, yaml_config, 'games/{}_{}.h5'.format(name, time.strftime('%Y%m%d_%H%M%S'))))
    storage_process.start()

    logging.info('started queue')

    inputs = [0,] * 8

    while queue.empty():
        logging.info('loop')
        if video.grab():
            logging.info('video grab')

            r, f = video.retrieve()

            agent.new_frame(f)
            temp_inputs = agent.get_inputs()

            if temp_inputs is not None:
                inputs = temp_inputs
                motor.control(inputs)

            pygame.surfarray.blit_array(screen, f)
            pygame.display.update()

            storage_queue.put((f, inputs))


    queue.get()
    storage_queue.put((None, None))
    storage_process.join()
    motor.resetEmulation(False)
    motor.disconnect()
    pygame.quit()