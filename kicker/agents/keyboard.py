import pygame

from kicker.agents.agent import Agent


class KeyboardAgent(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.keymap = {
            pygame.K_a: (1, 1),  pygame.K_s: (3, 1),  pygame.K_d: (5, 1),  pygame.K_f: (7, 1),
            pygame.K_q: (1, -1), pygame.K_w: (3, -1), pygame.K_e: (5, -1), pygame.K_r: (7, -1),
            pygame.K_j: (0, 1),  pygame.K_k: (2, 1),  pygame.K_l: (4, 1),  pygame.K_SEMICOLON: (6, 1),
            pygame.K_u: (0, -1), pygame.K_i: (2, -1), pygame.K_o: (4, -1), pygame.K_p: (6, -1)
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keymap:
                self.keypress(event)

        if event.type == pygame.KEYUP:
            if event.key in self.keymap:
                self.keyrelease(event)

    def keypress(self, event):
        t = self.keymap[event.key]
        if self.inputs[t[0]] != t[1]:
            self.inputs[t[0]] = t[1]
            self.inputs_changed = True

    def keyrelease(self, event):
        t = self.keymap[event.key]
        if self.inputs[t[0]] == t[1]:
            self.inputs[t[0]] = 0
            self.inputs_changed = True
