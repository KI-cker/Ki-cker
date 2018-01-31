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
python tools/score_training_data.py
```
This process produces then a file `train/training_data.h5` which contains the necessary information to train a neural net.

## Training

Training is still being implemented. In a python shell it can be achieved via
```
from kicker.train import DataProvider
d = DataProvider()

from kicker.train import Trainer
from kicker import NeuralNet
nn = NeuralNet(24, (320, 480, 2))

t = Trainer(nn)

for _ in range(100):
    s = d.get_batch()
    print(t.train_step(s)[1])
    
nn.save()
```
This updates `model.h5` with 100 training iterations.