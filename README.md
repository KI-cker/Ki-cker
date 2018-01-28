# KI:cker

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
python tools/filter_good_games.py
```
Then one can proceed to score the game with
```
python tools/score_training_data.py
```
This process produces then a file `train/training_data.h5` which contains the necessary information to train a neural net.