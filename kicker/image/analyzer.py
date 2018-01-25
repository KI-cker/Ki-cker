import numpy as np
import cv2

class Analyzer():
    def __init__(self, config):
        self.config = config
        self.coords = self.config['coordinates']
        self.positions = ['goal', 'defense', 'center', 'offense']
        self.ball_template = np.array([
               [   0,   0,   0,   0,   0, 255,   0, 255,   0,   0,   0,   0,   0,   0,   0],
               [   0,   0,   0, 255, 255,   0, 255,   0, 255, 255, 255, 255,   0,   0,   0],
               [   0,   0, 255, 255,   0,   0,   0,   0,   0,   0,   0, 255, 255,   0,   0],
               [   0, 255, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255,   0],
               [   0, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255,   0],
               [ 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255],
               [ 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255],
               [ 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255],
               [ 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255],
               [ 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255],
               [ 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255],
               [ 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255],
               [ 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255,   0],
               [ 255, 255,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255,   0],
               [   0, 255, 255,   0,   0,   0,   0,   0,   0,   0,   0, 255, 255,   0,   0],
               [   0,   0, 255, 255,   0,   0,   0,   0,   0,   0, 255, 255,   0,   0,   0],
               [   0,   0,   0, 255, 255, 255, 255, 255, 255, 255, 255,   0,   0,   0,   0]], dtype=np.uint8)

    def extract_table(self, frame, shape, offset_x=0, offset_y=0):
        width, height = shape

        coords = self.config['coordinates']
        pts1 = np.float32([
            coords['bottom_left_corner'],
            coords['top_left_corner'],
            coords['bottom_right_corner'],
            coords['top_right_corner']] + np.float32([[offset_x, offset_y],
                                                      [offset_x, offset_y],
                                                      [offset_x, offset_y],
                                                      [offset_x, offset_y]]))

        pts2 = np.float32([[0, 0], [0, height], [width, 0], [width, height]])

        M = cv2.getPerspectiveTransform(pts1, pts2)

        table_area = cv2.warpPerspective(frame, M, shape)

        return table_area

    def _can_move(self, frame, position, direction):
        p = position + '_' + direction
        # print((p, frame[self.coords[p][1], self.coords[p][0]]))
	return True

    def get_possible_moves(self, frame):
        return {p: [self._can_move(frame, p, 'left'), self._can_move(frame, p, 'right')] for p in self.positions}

    def add_circles_to_limiters(self, img):
        positions = [p for name in self.positions for p in [name + '_left', name + '_right']]
        img = img.copy()

        for p in positions:
            circle_color = (255, 0, 0)

            if self._can_move(img, p.split('_')[0], p.split('_')[1]):
                circle_color = (0, 255, 0)

            cv2.circle(img, tuple(self.coords[p]), 2, circle_color, 3)

        return img

    def compute_ball_center(self, frame):
        frame_canny = cv2.Canny(frame[:, :, 1], 320, 340)
        res = cv2.matchTemplate(frame_canny, self.ball_template, cv2.TM_CCOEFF)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        return (max_val, max_loc[0] + 8, max_loc[1] + 8)

