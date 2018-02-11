from matplotlib import pyplot, cm, gridspec
import numpy as np
import seaborn as sns

from kicker.train import DataProvider, Parser
from kicker import NeuralNet

# d = DataProvider(return_observations=True, filename='train/training_data_new.h5')
# s = d.get_batch()
#
nn = NeuralNet(23, (320, 480, 2))


fig  = pyplot.figure(figsize=(10, 8))

outer = gridspec.GridSpec(2, 1)

titles = ['Goal Radial', 'Goal Lateral', 'Defense Radial', 'Defense Lateral', 'Center Radial', 'Center Lateral', 'Attack Radial', 'Attack Lateral']

def show_prediction(before, now, after):
    fig.clf()
    inner = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=outer[0])
    axes = [pyplot.Subplot(fig, inner[j]) for j in range(3)]

    observation = np.concatenate((before[:,:,1].reshape((320, 480, 1)), now[:,:,1].reshape((320, 480, 1))), axis=2)
    prediction = nn.predict_single(observation).reshape(8, 3)
    axes[0].axis('off')
    axes[0].imshow(before, cmap = cm.Greys_r)
    axes[1].axis('off')
    axes[1].imshow(now, cmap = cm.Greys_r)
    axes[2].axis('off')
    axes[2].imshow(after, cmap = cm.Greys_r)

    for j in range(3):
        fig.add_subplot(axes[j])

    inner_plots = gridspec.GridSpecFromSubplotSpec(1, 8, subplot_spec=outer[1])

    for j in range(8):
        axes = pyplot.Subplot(fig, inner_plots[j])
        sns.barplot(y= prediction[j,:] - np.min(prediction[j,:]), x=['Backward', 'Null', 'Forward'],ax=axes)
        axes.set_title(titles[j])
        fig.add_subplot(axes)

    # print(prediction)
    print(np.argmax(prediction, axis=1) - np.ones(8))
    fig.show()
    pyplot.waitforbuttonpress(0)
    # input('press enter')
    # pyplot.close()

parser = Parser(filename='train/Fabian_20180209_133730.h5')

for game_name in parser.file:
    table_frames, positions, actions, scores = parser.get_game_data(game_name)

    length = len(table_frames)

    for j in range(1, length - 1):
        show_prediction(table_frames[j-1], table_frames[j], table_frames[j+1])