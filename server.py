import logging
import cv2
import time
from multiprocessing import Process, Queue

from flask import Flask, render_template, redirect, url_for, request, Response

from kicker.server.worker import worker

logging.basicConfig(filename='kicker.log', level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s')
logging.info("Fussball ist wie Schach nur ohne Wuerfel")

from glob import glob

process = None

stop_queue = Queue()
video_queue = Queue()
app = Flask('__name__', static_url_path='/assets',
            static_folder='templates/assets')


@app.route('/')
def index():
    global process
    if not process:
        models = glob('models/model_*.h5')
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
    global process, stop_queue, video_queue

    name = request.form['name']
    model = request.form['model']
    randomness = float(request.form['randomness']) / 100.0

    print('Starting. Name {}    Model {}    Randomness {}'.format(
        name, model, randomness))

    process = Process(target=worker, args=(
        stop_queue, video_queue, name, model, randomness))
    process.start()

    return redirect(url_for('index'))


def generate_video(video_queue):
    font = cv2.FONT_HERSHEY_SIMPLEX
    start_time = time.time()
    number = 1
    frame = None
    while True:
        while not video_queue.empty():
            number = number + 1
            frame = video_queue.get()

        if frame is not None:
            time_diff = time.time() - start_time
            cv2.putText(frame, '{}'.format(time_diff),
                        (10, 50), font, 1, (255, 255, 255))
            cv2.putText(frame, 'FPS {}'.format(float(number) /
                                               time_diff), (10, 100), font, 1, (255, 255, 255))
            jpeg_frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg_frame + b'\r\n')


@app.route('/video')
def video_feed():
    return Response(generate_video(video_queue),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
