import logging
import random
import numpy as np
import math

logger = logging.getLogger('Memory')


class BinnedData:
    def __init__(self):
        self.number_of_bins = 20
        self.delta_min = 0.01
        self.unseen_data = []

        self.bins = [[] for _ in range(self.number_of_bins)]
        self.probability_bins = [
            (0.04 * 2 ** k) ** 0.5 for k in range(self.number_of_bins)]

        self.weight_unseen = 0
        self.weight_bins = [0 for _ in range(self.number_of_bins)]
        self.total_weight = 0

        self.indices = None

    def log_statistics(self):
        logger.info('MEMORY: unseen %d, total %d', len(self.unseen_data),
                    np.sum([len(b) for b in self.bins]))
        for k in range(self.number_of_bins):
            logger.info('MEMORY: Bin %d: %10d', k, len(self.bins[k]))

    def add_unseen_data(self, new_data):
        self.unseen_data = self.unseen_data + new_data
        logger.info('MEMORY: new size %d', len(self.unseen_data))

    def update_weight(self):
        self.weight_unseen = len(self.unseen_data)
        self.weight_bins = [self.probability_bins[k] *
                            len(self.bins[k]) for k in range(self.number_of_bins)]
        self.total_weight = self.weight_unseen + np.sum(self.weight_bins)

    def sample(self, batch_size=32):
        self.update_weight()
        self.indices = np.sort([random.random() for _ in range(batch_size)])

        return [self.get(i) for i in self.indices.tolist()]

    def update_with_deltas(self, deltas):
        new_elements_in_bins = [[] for _ in range(self.number_of_bins)]

        for k in range(len(deltas)):
            target_bin = self.determine_target_bin(deltas[k])
            new_elements_in_bins[target_bin].append(self.get(self.indices[k]))

        indices = self.indices.tolist()
        indices.reverse()

        for i in indices:
            self.remove(i)

        for k in range(self.number_of_bins):
            self.bins[k].extend(new_elements_in_bins[k])

    def determine_target_bin(self, delta):
        percentage = delta / self.delta_min
        if percentage < 1:
            return 0

        return min(int(math.log(percentage) / math.log(2)),
                   self.number_of_bins - 1)

    def get(self, i):
        index = i * self.total_weight

        if index < self.weight_unseen:
            return self.unseen_data[int(index)]

        index = index - self.weight_unseen

        for k in range(self.number_of_bins):
            if index < self.weight_bins[k]:
                return self.bins[k][int(index / self.probability_bins[k])]
            else:
                index = index - self.weight_bins[k]

    def remove(self, i):
        index = i * self.total_weight

        if index < self.weight_unseen:
            try:
                del self.unseen_data[int(index)]
            except IndexError as err:
                logger.error(err)
            return

        index = index - self.weight_unseen

        for k in range(self.number_of_bins):
            if index < self.weight_bins[k]:
                try:
                    del self.bins[k][int(index / self.probability_bins[k])]
                except IndexError as err:
                    logger.error(err)
                return
            else:
                index = index - self.weight_bins[k]
