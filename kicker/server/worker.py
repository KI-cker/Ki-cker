import logging
import time
import json
import numpy as np
from datetime import datetime
import os

import cv2
import yaml
from multiprocessing import Queue, Process

from kicker.opcua_motor import motor_worker
from kicker.storage import storage_worker

def worker(queue, video_queue, name, model, randomness):
    import tensorflow as tf
    from kicker.agents.neural_net_agent import NeuralNetAgent
    import keras.backend.tensorflow_backend as KTF

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
    filename = '{}_{}.h5'.format(name, time.strftime('%Y%m%d_%H%M%S'))
    storage_process = Process(target=storage_worker, args=(storage_queue, yaml_config, filename))
    storage_process.start()

    logging.info('started queue')

    motor_queue = Queue()
    motor_process = Process(target=motor_worker, args=(motor_queue,))
    motor_process.start()


    monitoring_queue = Queue()
    monitoring_process = Process(target=monitoring_worker, args=(monitoring_queue,))
    monitoring_process.start()

    logging.info('started control')

    inputs = [0,] * 8

    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


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
                inputs = temp_inputs

                motor_queue.put(inputs)
                monitoring_queue.put([frame, prediction])
            time_control = (time.time() - start_time) * 1000 - time_neural_net

            storage_queue.put((f, inputs))
            # video_queue.put(f)
            time_total = (time.time() - start_time) * 1000

            sock.sendto(json.dumps([time_neural_net, time_control, time_total]).encode(), ('localhost', 1883))


    queue.get()
    storage_queue.put((None, None))
    storage_process.join()

    os.rename(filename, 'games/' + filename)

    motor_queue.put(None)
    motor_process.join()
    monitoring_queue.put(None)
    monitoring_process.join()
    # motor.resetEmulation(False)

def monitoring_worker(queue):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        data = queue.get()
        if data is None:
            break
        if queue.empty():
            prediction = data[1].reshape(8, 3)
            img_enc = cv2.imencode('.jpg', np.swapaxes(data[0], 0, 1)[::-1,:,:])[1].tostring().encode('base64')
            sock.sendto(img_enc, ('localhost', 1882))
            sock.sendto(json.dumps(prediction.tolist()).encode(), ('localhost', 1881))

