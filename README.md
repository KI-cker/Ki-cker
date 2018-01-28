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