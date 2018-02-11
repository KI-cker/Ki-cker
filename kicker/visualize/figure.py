from matplotlib import pyplot, cm, gridspec
import numpy as np
import seaborn as sns


class Figure():
    def __init__(self):
        self.figure = pyplot.figure(figsize=(10, 8))

        self.outer = gridspec.GridSpec(2, 1)

        self.titles = ['Goal Radial', 'Goal Lateral', 'Defense Radial', 'Defense Lateral', 'Center Radial', 'Center Lateral',
                  'Attack Radial', 'Attack Lateral']

        self.inner = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=self.outer[0])
        self.inner_plots = gridspec.GridSpecFromSubplotSpec(1, 8, subplot_spec=self.outer[1])


    def plot(self, before, now, after, prediction):
        self.figure.clf()

        axes = [pyplot.Subplot(self.figure, self.inner[j]) for j in range(3)]

        axes[0].imshow(before, cmap=cm.Greys_r)
        axes[1].imshow(now, cmap=cm.Greys_r)
        axes[2].imshow(after, cmap=cm.Greys_r)

        for j in range(3):
            axes[j].axis('off')
            self.figure.add_subplot(axes[j])

        for j in range(8):
            axes = pyplot.Subplot(self.figure, self.inner_plots[j])
            sns.barplot(y=prediction[j, :] - np.min(prediction[j, :]), x=['Backward', 'Null', 'Forward'], ax=axes)
            axes.set_title(self.titles[j])
            self.figure.add_subplot(axes)

        self.figure.show()
        pyplot.waitforbuttonpress(0)
