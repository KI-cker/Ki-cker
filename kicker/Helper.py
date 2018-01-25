class Helper():

    def handle_forbidden_moves(self, possible_moves, actions):

        if not possible_moves['goal'][0] and actions[0] == -1:
            actions[0] = 0
        if not possible_moves['defense'][0] and actions[2] == -1:
            actions[2] = 0
        if not possible_moves['center'][0] and actions[4] == -1:
            actions[4] = 0
        if not possible_moves['offense'][0] and actions[6] == -1:
            actions[6] = 0

        if not possible_moves['goal'][1] and actions[0] == 1:
            actions[0] = 0
        if not possible_moves['defense'][1] and actions[2] == 1:
            actions[2] = 0
        if not possible_moves['center'][1] and actions[4] == 1:
            actions[4] = 0
        if not possible_moves['offense'][1] and actions[6] == 1:
            actions[6] = 0

        return actions