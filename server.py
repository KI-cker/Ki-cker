from flask import Flask, render_template, redirect, url_for, request, send_from_directory

import cv2
import yaml
import time

from kicker.opcua_motor import MotorController
from kicker.storage import storage_worker


from multiprocessing import Process, Queue
from time import sleep

import logging

logging.basicConfig(filename='kicker.log', level=logging.DEBUG, format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s')
logging.info("Fussball ist wie Schach nur ohne Wuerfel")

from glob import glob

def worker(queue, name, model, randomness):
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

            storage_queue.put((f, inputs))


    queue.get()
    storage_queue.put((None, None))
    storage_process.join()
    motor.resetEmulation(False)
    motor.disconnect()



process = None

stop_queue = Queue()
app = Flask('__name__', static_url_path='/assets', static_folder='templates/assets')

@app.route('/')
def index():
    global process
    if not process:
        models = glob('models/*.h5')
        models.sort()
        models.reverse()
        return render_template('start.html', models=models)
    else:
        return render_template('stop.html')

@app.route('/stop')
def stop():
    global process, stop_queue
    print('Stopping')
    stop_queue.put('test')
    process_backup = process
    process = None
    process_backup.join()

    return redirect(url_for('index'))

@app.route('/start', methods=['POST'])
def start():
    global process, stop_queue

    name = request.form['name']
    model = request.form['model']
    randomness = float(request.form['randomness']) / 100.0

    print('Starting. Name {}    Model {}    Randomness {}'.format(name, model, randomness))

    process = Process(target=worker, args=(stop_queue, name, model, randomness))
    process.start()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
