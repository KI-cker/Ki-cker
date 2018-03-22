class Agent:
    def __init__(self):
        self.inputs_changed = False
        self.inputs = [0, ] * 8
        self.prediction = None

    def new_frame(self, frame):
        pass

    def get_inputs(self):
        if self.inputs_changed:
            self.inputs_changed = False
            return self.inputs, self.prediction
        else:
            return None, None

    def handle_event(self, event):
        pass
