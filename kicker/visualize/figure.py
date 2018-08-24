import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot, cm, gridspec
import numpy as np
import seaborn as sns


class Figure():
    def __init__(self, wait_for_button_press=True, show_images=True, visualize_q_value=False):

        self.titles = ['Goal Radial', 'Goal Lateral', 'Defense Radial', 'Defense Lateral', 'Center Radial', 'Center Lateral',
                  'Attack Radial', 'Attack Lateral']

        self.degrees_of_freedom = len(self.titles)

        if visualize_q_value:
            self.build_plot_for_q_value_visualization()
        elif show_images:
            self.build_plot_with_images()
        else:
            self.build_plot_without_images()

        self.wait_for_button_press = wait_for_button_press
        self.show_images = show_images
        self.visualize_q_value = visualize_q_value

        self.history = [[] for _ in range(self.degrees_of_freedom)]

    def build_plot_with_images(self):
        self.figure = pyplot.figure(figsize=(10, 8))
        self.outer = gridspec.GridSpec(3, 1)
        self.inner = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=self.outer[0])
        self.inner_plots = gridspec.GridSpecFromSubplotSpec(1, self.degrees_of_freedom, subplot_spec=self.outer[1])
        self.history_plots = gridspec.GridSpecFromSubplotSpec(1, int(self.degrees_of_freedom / 2), subplot_spec=self.outer[2])

    def build_plot_for_q_value_visualization(self):
        self.figure = pyplot.figure(figsize=(10, 8))
        self.outer = gridspec.GridSpec(1, 1)
        self.history_plots = gridspec.GridSpecFromSubplotSpec(1, int(self.degrees_of_freedom / 2), subplot_spec=self.outer[0])

    def plot(self, before, now, after, prediction):
        self.figure.clf()

        if self.show_images and not(self.visualize_q_value):
            axes = [pyplot.Subplot(self.figure, self.inner[j]) for j in range(3)]

            axes[0].imshow(before, cmap=cm.Greys_r)
            axes[1].imshow(now, cmap=cm.Greys_r)
            axes[2].imshow(after, cmap=cm.Greys_r)

            for j in range(3):
                axes[j].axis('off')
                self.figure.add_subplot(axes[j])

        for j in range(self.degrees_of_freedom):
            if not(self.visualize_q_value):
                axes = pyplot.Subplot(self.figure, self.inner_plots[j])
                sns.barplot(y=prediction[j, :] - np.min(prediction[j, :]), x=['Backward', 'Null', 'Forward'], ax=axes)
                axes.set_title(self.titles[j])
                self.figure.add_subplot(axes)

            self.history[j].append(np.max(prediction[j, :]))

        for j in range(int(self.degrees_of_freedom / 2)):
            axes_history = pyplot.Subplot(self.figure, self.history_plots[j])
            l = len(self.history[0][-100:])
            axes_history.plot(range(l), self.history[2 * j][-100:], range(l), self.history[2 * j + 1][-100:])
            self.figure.add_subplot(axes_history)

        if not(self.visualize_q_value):
            self.figure.show()
            if self.wait_for_button_press:
                pyplot.waitforbuttonpress(0)
            else:
                pyplot.waitforbuttonpress(0.1)

    def build_plot_without_images(self):
        self.figure = pyplot.figure(figsize=(10, 8))
        self.outer = gridspec.GridSpec(2, 1)
        self.inner_plots = gridspec.GridSpecFromSubplotSpec(1, self.degrees_of_freedom, subplot_spec=self.outer[0])
        self.history_plots = gridspec.GridSpecFromSubplotSpec(1, self.degrees_of_freedom, subplot_spec=self.outer[1])
