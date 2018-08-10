# KI:cker
## Preparation

Add the current directory to the search path via
```
export PYTHONPATH=$(pwd)
``` 
install requirements via
```
pip install -r requirements.txt
```
Automatic code formatting via
```
autopep8 -r --in-place .
```

## Preprocessing for training

Extract the table region via
```
python tools/add_table_frames_to_h5py.py -i filename
```
Add ball positions
```
python tools/neural_net_detection.py -f tools/frozen_inference_graph.pb -i train/games.h5
```
Filter out the good games. This scripts weeds out games, where here are few distinct ball positions detected.
```
python tools/filter_good_games.py -i $INPUT_FILE -o OUTPUT_FILE
```
Then one can proceed to score the game with
```
python tools/score_training_data.py -i $INPUT_FILE
```
This process produces then a file `train/training_data.h5` which contains the necessary information to train a neural net.

## Training

Training can be  corun for 1000 steps via the
```
python tools/train_1000.py
```
This updates `model.h5` with 1000 training iterations.

Running
```
python tools/analyze_model.py model.h5
```
generates graphs displaying the distribution of the weights. These should approach smooth curvers during training.

## Visualisation
With
```
python tools/inspect_data.py
```
one can visualize what the neural net sees. One sees the three subsequent frames from the collected data set, and the actions that the neural net would perform in the form
```
[gr, gl, dr, dl, cr, cl, ar, al]
```
where g = goal, d = defense, c = center, a = attack and r = rotation, l = lateral. 0 corresponds to no movement, 1 to forward, -1 to backward.

The tool
```
python tools/view_game_file.py
```
shows a specific game. Useful for inspecting the progress of neural net training.

## Tensorboard
After training via `python tools/train_1000.py`, one can use tensorboard to visualize
the training via
```
tensorboard --logdir=tensorboard_logdir
```
