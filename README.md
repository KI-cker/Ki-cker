# KI:cker
## Preparation

Add the current directory to the search path via
```
export PYTHONPATH=$(pwd)
``` 

## Preprocessing for training

Extract the table region via
```
python tools/add_table_frames_to_h5py.py
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