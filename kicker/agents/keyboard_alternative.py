import pygame

from kicker.agents.agent import Agent


class KeyboardAgentAlternative(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.pressed = []
        self.tracked = [
            pygame.K_DOWN,
            pygame.K_UP,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_a,
            pygame.K_1,
            pygame.K_s,
            pygame.K_2,
            pygame.K_d,
            pygame.K_3,
            pygame.K_f,
            pygame.K_4
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.tracked:
                self.pressed.append(event.key)
            self.update_inputs()
        elif event.type == pygame.KEYUP:
            while event.key in self.pressed:
                self.pressed.remove(event.key)
            self.update_inputs()

    def update_inputs(self):
        translationSignal = (pygame.K_DOWN in self.pressed) - (pygame.K_UP in self.pressed)
        rotationSignal = (pygame.K_RIGHT in self.pressed) - (pygame.K_LEFT in self.pressed)
        goalie = (pygame.K_a in self.pressed) or (pygame.K_1 in self.pressed)
        defense = (pygame.K_s in self.pressed) or (pygame.K_2 in self.pressed)
        midfield = (pygame.K_d in self.pressed) or (pygame.K_3 in self.pressed)
        offense = (pygame.K_f in self.pressed) or (pygame.K_4 in self.pressed)
        self.inputs = [
            goalie * translationSignal,
            goalie * rotationSignal,
            defense * translationSignal,
            defense * rotationSignal,
            midfield * translationSignal,
            midfield * rotationSignal,
            offense * translationSignal,
            offense * rotationSignal
        ]
        self.inputs_changed = True
