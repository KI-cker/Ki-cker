import cv2

from kicker.image import Analyzer



class Converter:
    def __init__(self, parser, game, shape=(480, 320)):
        self.parser = parser
        self.game = game
        self.shape = shape

        self.analyzer = Analyzer(self.parser.get_config(self.game))

    def get_table_frame(self, index):
        frame = self.parser.get_frame(self.game, index)
        return self.analyzer.extract_table(frame, self.shape)

    def get_table_frames(self):
        number = self.parser.get_number_of_frames(self.game)

        return [self.get_table_frame(i) for i in range(number)]

    def get_table_frames_encoded(self):
        return [cv2.imencode('.jpg', i)[1].tostring() for i in self.get_table_frames()]