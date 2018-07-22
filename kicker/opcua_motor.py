import logging

from kicker.opcua.opcua_controller import OpcuaController

logging.basicConfig(filename='opcua.log', level=logging.ERROR,
                    format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s')


def motor_worker(queue):
    motor = MotorController()
    motor.resetEmulation()

    while True:
        command = queue.get()

        if command is None:
            break

        if queue.empty():
            motor.control(command)

    motor.disconnect()


class MotorController(OpcuaController):
    def __init__(self):
        super(MotorController, self).__init__()
        self.connect()

        self.last_action = [0, 0, 0, 0, 0, 0, 0, 0]
        self.NO_ACTION = 0  # a magic number

    def translation(self, axisno, direction):
        if direction == 0:
            self.stopJog_Trans(axisno)
        elif direction == 1:
            self.positiveJog_Trans(axisno)
        else:
            self.negativeJog_Trans(axisno)

    def rotation(self, axisno, direction):
        if direction == 0:
            self.stopJog_Rot(axisno)
        elif direction == 1:
            self.positiveJog_Rot(axisno)
        else:
            self.negativeJog_Rot(axisno)

    def getDiffToLastAction(self, action):
        diff = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, 8):
            if self.last_action[i] != action[i]:
                diff[i] = 1
            else:
                diff[i] = self.NO_ACTION

        return diff

    def control(self, action):
        diffAction = self.getDiffToLastAction(action)
        self.last_action = action[:]

        # # print action
        # Sturm
        if diffAction[6] != self.NO_ACTION:
            self.rotation(4, action[6])
        if diffAction[7] != self.NO_ACTION:
            self.translation(4, action[7])

        # Mittelfeld
        if diffAction[4] != self.NO_ACTION:
            self.rotation(3, action[4])
        if diffAction[5] != self.NO_ACTION:
            self.translation(3, action[5])

        # Verteidiger
        if diffAction[2] != self.NO_ACTION:
            self.rotation(2, action[2])
        if diffAction[3] != self.NO_ACTION:
            self.translation(2, action[3])

        # Torwart
        if diffAction[0] != self.NO_ACTION:
            self.rotation(1, action[0])
        if diffAction[1] != self.NO_ACTION:
            self.translation(1, action[1])

    def stop_all(self):
        self.translation(1, 0)
        self.translation(2, 0)
        self.translation(3, 0)
        self.translation(4, 0)
        self.rotation(1, 0)
        self.rotation(2, 0)
        self.rotation(3, 0)
        self.rotation(4, 0)
