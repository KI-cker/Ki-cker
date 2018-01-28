import h5py

f = h5py.File('train/training_data.h5')

for game_name in f:
    game = f[game_name]

    print("Processing {}".format(game_name))

    if 'scores' not in game and 'ball_pos' in game:
        scores = [0]

        positions = game['ball_pos']
        positions_x = [p[0] for p in positions]

        for i in range(1, len(positions)):
            if positions_x[i] - positions_x[i - 1] < 0:
                scores.append(1)
            else:
                scores.append(-1)

        game['scores'] = scores