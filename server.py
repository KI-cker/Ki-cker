from flask import Flask, render_template, redirect, url_for, request

from multiprocessing import Process, Queue
from time import sleep

import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)

from glob import glob

def worker(queue):
    j = 0
    while queue.empty():
        logging.info('text {}'.format(j))
        sleep(1)
        j = j + 1
    print(queue.get())



process = None

stop_queue = Queue()
app = Flask('__name__')

@app.route('/')
def index():
    global process
    if not process:
        models = glob('models/*.h5')
        models.sort()
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
    randomness = request.form['randomness']

    print('Starting. Name {}    Model {}    Randomness {}'.format(name, model, randomness))

    process = Process(target=worker, args=(stop_queue,))
    process.start()

    return redirect(url_for('index'))

