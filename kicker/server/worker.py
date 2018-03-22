import logging
import time
import json
import numpy as np
from datetime import datetime

import cv2
import yaml
from multiprocessing import Queue, Process

from kicker.opcua_motor import motor_worker
from kicker.storage import storage_worker

def worker(queue, video_queue, name, model, randomness):
    import tensorflow as tf
    from kicker.agents.neural_net_agent import NeuralNetAgent
    import keras.backend.tensorflow_backend as KTF

    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    KTF.set_session(sess)

    logging.info('started session')

    agent = NeuralNetAgent(randomness=randomness, neural_net_filename=model)

    logging.info('started neural net')

    video = cv2.VideoCapture(1)

    logging.info('started video')

    with open('config.yml', 'r') as f:
        yaml_config = yaml.load(f)

    storage_queue = Queue()
    storage_process = Process(target=storage_worker, args=(storage_queue, yaml_config, 'games/{}_{}.h5'.format(name, time.strftime('%Y%m%d_%H%M%S'))))
    storage_process.start()

    logging.info('started queue')

    motor_queue = Queue()
    motor_process = Process(target=motor_worker, args=(motor_queue,))
    motor_process.start()

    logging.info('started control')

    inputs = [0,] * 8

    while queue.empty():
        logging.info('loop')
        if video.grab():
            start_time = time.time()
            logging.info('video grab')
            start_time = time.time()

            r, f = video.retrieve()

            frame  = agent.new_frame(f)
            temp_inputs, prediction = agent.get_inputs()

            time_neural_net = (time.time() - start_time) * 1000
            if temp_inputs is not None:
                prediction = prediction[0].reshape(8,3)
                img_enc = cv2.imencode('.jpg', np.swapaxes(frame, 0, 1))[1].tostring().encode('base64')
                sock.sendto(img_enc, ('localhost', 1882))
                sock.sendto(json.dumps(prediction.tolist()).encode(), ('localhost', 1881))
                inputs = temp_inputs

                motor_queue.put(inputs)
            time_control = (time.time() - start_time) * 1000 - time_neural_net

            storage_queue.put((f, inputs))
            # video_queue.put(f)
            time_total = (time.time() - start_time) * 1000

            sock.sendto(json.dumps([time_neural_net, time_control, time_total]).encode(), ('localhost', 1883))


    queue.get()
    storage_queue.put((None, None))
    storage_process.join()
    motor_queue.put(None)
    motor_process.join()
    # motor.resetEmulation(False)
