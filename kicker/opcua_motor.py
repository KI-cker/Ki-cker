import time
from opcua import Client
from opcua import ua
import logging

logging.basicConfig(filename='opcua.log', level=logging.ERROR, format='%(asctime)s %(filename)s %(lineno)d %(levelname)s %(message)s')


#handler for subscriptions
class SubScriptionHandler(object):
    def datachange_notification(self, node, val, data):
        value = data.monitored_item.Value.Value.Value
        nodeid = data.subscription_data.node.nodeid.Identifier
        timestamp = data.monitored_item.Value.ServerTimestamp
        logging.debug("nodeid: ", nodeid, ";value:",value,";timestamp:",timestamp)
        logging.debug("Subscription",node, val, dir(data.subscription_data.node.nodeid))
        ###Implement your target-method here!####
#end handler for subscriptions


#specify variable-id's
vars_namespace = 2                                                      #yet, only logic variables used ==> only one namespace, if variables from multiply ns used ==> change in src-code

#program control variables
startEmulation  =   ["Application.GVLpython.bAutomatic",2]           #Variable-symbol-path, namespace (ns=2;Application.GVLpython.rABC) ==> [Application.GVLpython.rABC, 2]
initDone        =   False

PosMode_Ack_Rot_Tor 			= ["Application.GVLpython.bPosModeAck_Rot_Tor",2]
PosMode_Ack_Rot_Verteidiung 	= ["Application.GVLpython.bPosModeAck_Rot_Verteidigung",2]
PosMode_Ack_Rot_Mittelfeld 		= ["Application.GVLpython.bPosModeAck_Rot_Mittelfeld",2]
PosMode_Ack_Rot_Sturm 			= ["Application.GVLpython.bPosModeAck_Rot_Sturm",2]
PosMode_Ack_Trans_Tor 			= ["Application.GVLpython.bPosModeAck_Trans_Tor",2]
PosMode_Ack_Trans_Verteidiung 	= ["Application.GVLpython.bPosModeAck_Trans_Verteidigung",2]
PosMode_Ack_Trans_Mittelfeld 	= ["Application.GVLpython.bPosModeAck_Trans_Mittelfeld",2]
PosMode_Ack_Trans_Sturm 		= ["Application.GVLpython.bPosModeAck_Trans_Sturm",2]


#end program control variables

#motion variables to set
Axis1_Rot_JogNegative       =       ["Application.GVLpython.bNegative_jog_Rot_Tor",2]
Axis1_Rot_JogPositive       =       ["Application.GVLpython.bPositive_jog_Rot_Tor",2]
ActualPosition_Axis1_Rot    =       ["Application.GVLpython.rActualPosition_Rot_Tor",2]
ActualVelocity_Axis1_Rot    =       ["Application.GVLpython.rActualVelocity_Rot_Tor",2]
Axis1_Rot_lower_limit_vel   =       ["Application.GVLpython.rLimitVelRot",2]
Axis1_Rot_upper_limit_vel   =       ["Application.GVLpython.rLimitVelRot",2]
Axis1_Rot_abs_limit_acc     =       ["Application.GVLpython.rLimitAccRot",2]

Axis1_Trans_JogNegative     =       ["Application.GVLpython.bNegative_jog_Trans_Tor",2]
Axis1_Trans_JogPositive     =       ["Application.GVLpython.bPositive_jog_Trans_Tor",2]
ActualPosition_Axis1_Trans  =       ["Application.GVLpython.rActualPosition_Trans_Tor",2]
ActualVelocity_Axis1_Trans  =       ["Application.GVLpython.rActualVelocity_Trans_Tor",2]
Axis1_Trans_lower_limit_vel =       ["Application.GVLpython.rLimitVelTrans",2]
Axis1_Trans_upper_limit_vel =       ["Application.GVLpython.rLimitVelTrans",2]
Axis1_Trans_abs_limit_acc   =       ["Application.GVLpython.rLimitAccTrans",2]

Axis2_Rot_JogNegative       =       ["Application.GVLpython.bNegative_jog_Rot_Verteidigung",2]
Axis2_Rot_JogPositive       =       ["Application.GVLpython.bPositive_jog_Rot_Verteidigung",2]
ActualPosition_Axis2_Rot    =       ["Application.GVLpython.rActualPosition_Rot_Verteidigung",2]
ActualVelocity_Axis2_Rot    =       ["Application.GVLpython.rActualVelocity_Rot_Verteidigung",2]
Axis2_Rot_lower_limit_vel   =       ["Application.GVLpython.rLimitVelRot",2]
Axis2_Rot_upper_limit_vel   =       ["Application.GVLpython.rLimitVelRot",2]
Axis2_Rot_abs_limit_acc     =       ["Application.GVLpython.rLimitAccRot",2]


Axis2_Trans_JogNegative     =       ["Application.GVLpython.bNegative_jog_Trans_Verteidigung",2]
Axis2_Trans_JogPositive     =       ["Application.GVLpython.bPositive_jog_Trans_Verteidigung",2]
ActualPosition_Axis2_Trans  =       ["Application.GVLpython.rActualPosition_Trans_Verteidigung",2]
ActualVelocity_Axis2_Trans  =       ["Application.GVLpython.rActualVelocity_Trans_Verteidigung",2]
Axis2_Trans_lower_limit_vel =       ["Application.GVLpython.rLimitVelTrans",2]
Axis2_Trans_upper_limit_vel =       ["Application.GVLpython.rLimitVelTrans",2]
Axis2_Trans_abs_limit_acc   =       ["Application.GVLpython.rLimitAccTrans",2]

Axis3_Rot_JogNegative       =       ["Application.GVLpython.bNegative_jog_Rot_Mittelfeld",2]
Axis3_Rot_JogPositive       =       ["Application.GVLpython.bPositive_jog_Rot_Mittelfeld",2]
ActualPosition_Axis3_Rot    =       ["Application.GVLpython.rActualPosition_Rot_Mittelfeld",2]
ActualVelocity_Axis3_Rot    =       ["Application.GVLpython.rActualVelocity_Rot_Mittelfeld",2]
Axis3_Rot_lower_limit_vel   =       ["Application.GVLpython.rLimitVelRot",2]
Axis3_Rot_upper_limit_vel   =       ["Application.GVLpython.rLimitVelRot",2]
Axis3_Rot_abs_limit_acc     =       ["Application.GVLpython.rLimitAccRot",2]


Axis3_Trans_JogNegative     =       ["Application.GVLpython.bNegative_jog_Trans_Mittelfeld",2]
Axis3_Trans_JogPositive     =       ["Application.GVLpython.bPositive_jog_Trans_Mittelfeld",2]
ActualPosition_Axis3_Trans  =       ["Application.GVLpython.rActualPosition_Trans_Mittelfeld",2]
ActualVelocity_Axis3_Trans  =       ["Application.GVLpython.rActualVelocity_Trans_Mittelfeld",2]
Axis3_Trans_lower_limit_vel =       ["Application.GVLpython.rLimitVelTrans",2]
Axis3_Trans_upper_limit_vel =       ["Application.GVLpython.rLimitVelTrans",2]
Axis3_Trans_abs_limit_acc   =       ["Application.GVLpython.rLimitAccTrans",2]

Axis4_Rot_JogNegative       =       ["Application.GVLpython.bNegative_jog_Rot_Sturm",2]
Axis4_Rot_JogPositive       =       ["Application.GVLpython.bPositive_jog_Rot_Sturm",2]
ActualPosition_Axis4_Rot    =       ["Application.GVLpython.rActualPosition_Rot_Sturm",2]
ActualVelocity_Axis4_Rot    =       ["Application.GVLpython.rActualVelocity_Rot_Sturm",2]
Axis4_Rot_lower_limit_vel   =       ["Application.GVLpython.rLimitVelRot",2]
Axis4_Rot_upper_limit_vel   =       ["Application.GVLpython.rLimitVelRot",2]
Axis4_Rot_abs_limit_acc     =       ["Application.GVLpython.rLimitAccRot",2]

Axis4_Trans_JogNegative     =       ["Application.GVLpython.bNegative_jog_Trans_Sturm",2]
Axis4_Trans_JogPositive     =       ["Application.GVLpython.bPositive_jog_Trans_Sturm",2]
ActualPosition_Axis4_Trans  =       ["Application.GVLpython.rActualPosition_Trans_Sturm",2]
ActualVelocity_Axis4_Trans  =       ["Application.GVLpython.rActualVelocity_Trans_Sturm",2]
Axis4_Trans_lower_limit_vel =       ["Application.GVLpython.rLimitVelTrans",2]
Axis4_Trans_upper_limit_vel =       ["Application.GVLpython.rLimitVelTrans",2]
Axis4_Trans_abs_limit_acc   =       ["Application.GVLpython.rLimitAccTrans",2]

AxisRot1        = [Axis1_Rot_JogNegative, Axis1_Rot_JogPositive,ActualPosition_Axis1_Rot,ActualVelocity_Axis1_Rot,Axis1_Rot_lower_limit_vel,Axis1_Rot_upper_limit_vel,Axis1_Rot_abs_limit_acc]
AxisTrans1      = [Axis1_Trans_JogNegative, Axis1_Trans_JogPositive, ActualPosition_Axis1_Trans, ActualVelocity_Axis1_Trans,Axis1_Trans_lower_limit_vel,Axis1_Trans_upper_limit_vel,Axis1_Trans_abs_limit_acc]
Axis1 = [AxisRot1,AxisTrans1]
AxisRot2        = [Axis2_Rot_JogNegative, Axis2_Rot_JogPositive, ActualPosition_Axis2_Rot, ActualVelocity_Axis2_Rot,Axis2_Rot_lower_limit_vel,Axis2_Rot_upper_limit_vel,Axis2_Rot_abs_limit_acc]
AxisTrans2      = [Axis2_Trans_JogNegative,Axis2_Trans_JogPositive, ActualPosition_Axis2_Trans, ActualVelocity_Axis2_Trans,Axis2_Trans_lower_limit_vel,Axis2_Trans_upper_limit_vel,Axis2_Trans_abs_limit_acc]
Axis2 = [AxisRot2,AxisTrans2]
AxisRot3        = [Axis3_Rot_JogNegative, Axis3_Rot_JogPositive, ActualPosition_Axis3_Rot, ActualVelocity_Axis3_Rot,Axis3_Rot_lower_limit_vel,Axis3_Rot_upper_limit_vel,Axis3_Rot_abs_limit_acc]
AxisTrans3      = [Axis3_Trans_JogNegative, Axis3_Trans_JogPositive, ActualPosition_Axis3_Trans, ActualVelocity_Axis3_Trans,Axis3_Trans_lower_limit_vel,Axis3_Trans_upper_limit_vel,Axis3_Trans_abs_limit_acc]
Axis3 = [AxisRot3,AxisTrans3]
AxisRot4        = [Axis4_Rot_JogNegative, Axis4_Rot_JogPositive, ActualPosition_Axis4_Rot, ActualVelocity_Axis4_Rot,Axis4_Rot_lower_limit_vel,Axis4_Rot_upper_limit_vel,Axis4_Rot_abs_limit_acc]
AxisTrans4      = [Axis4_Trans_JogNegative, Axis4_Trans_JogPositive, ActualPosition_Axis4_Trans, ActualVelocity_Axis4_Trans,Axis4_Trans_lower_limit_vel,Axis4_Trans_upper_limit_vel,Axis4_Trans_abs_limit_acc]
Axis4 = [AxisRot4,AxisTrans4]
Axis = [Axis1,Axis2,Axis3,Axis4]


class MotorController:
    def __init__(self):
        self.client = Client("opc.tcp://192.168.42.20:4840")
        self.connect()


        self.last_action = [0, 0, 0, 0, 0, 0, 0, 0]
        self.NO_ACTION = 0 # a magic number

    def resetEmulation(self):
        var = self.client.get_node(ua.NodeId(resetEmulation[0], resetEmulation[1]))
        var.set_value(ua.Variant(True, ua.VariantType.Boolean))

    def connect(self):
        self.client.connect()
        root = self.client.get_root_node()
        if (root != ""):
            logging.info("Connection established")
            ack_axis1 = self.readValue_polling(PosMode_Ack_Rot_Tor[0], PosMode_Ack_Rot_Tor[1])
            ack_axis2 = self.readValue_polling(PosMode_Ack_Rot_Verteidiung[0], PosMode_Ack_Rot_Verteidiung[1])
            ack_axis3 = self.readValue_polling(PosMode_Ack_Rot_Mittelfeld[0], PosMode_Ack_Rot_Mittelfeld[1])
            ack_axis4 = self.readValue_polling(PosMode_Ack_Rot_Sturm[0], PosMode_Ack_Rot_Sturm[1])
            ack_axis5 = self.readValue_polling(PosMode_Ack_Trans_Tor[0], PosMode_Ack_Trans_Tor[1])
            ack_axis6 = self.readValue_polling(PosMode_Ack_Trans_Verteidiung[0], PosMode_Ack_Trans_Verteidiung[1])
            ack_axis7 = self.readValue_polling(PosMode_Ack_Trans_Mittelfeld[0], PosMode_Ack_Trans_Mittelfeld[1])
            ack_axis8 = self.readValue_polling(PosMode_Ack_Trans_Sturm[0], PosMode_Ack_Trans_Sturm[1])
            initDone = ack_axis1 and ack_axis2 and ack_axis3 and ack_axis4 and ack_axis5 and ack_axis6 and ack_axis7 and ack_axis8

            if (initDone != True):
                 logging.info("axis not ready yet or error")

            if (initDone == True):
                logging.info("axis ready")
        else:
            logging.info("Could not connect to server!")

    def readValue_polling(self, nodeId, namespace):
        var = self.client.get_node(ua.NodeId(nodeId, namespace))
        return var.get_value()

    def writeBooleanValue(self, nodeId, namespace, value):
        var = self.client.get_node(ua.NodeId(nodeId, namespace))
        var.set_value(ua.Variant(value, ua.VariantType.Boolean))

    def writeFloatValue(self, nodeId, namespace, value):
        var = self.client.get_node(ua.NodeId(nodeId, namespace))
        var.set_value(ua.Variant(value, ua.VariantType.Float))

    def disconnect(self):
        self.client.disconnect()

    def add_subscription(self, AxisNo, AxisType,
                         MeasurementType):  # AxisNo [1...4], AxisType ["Trans","Rot"], MeasurementType ["Vel","Pos"]
        if AxisType == "Rot":
            atype = 0
        if AxisType == "Trans":
            atype = 1
        if MeasurementType == "Pos":
            mtype = 2
        if MeasurementType == "Trans":
            mtype = 3
        nodeId = Axis[AxisNo - 1][atype][mtype][0]
        namespace = Axis[AxisNo - 1][atype][mtype][1]
        var = self.client.get_node(ua.NodeId(nodeId, namespace))
        handler = SubScriptionHandler()
        sub = self.client.create_subscription(50, handler)
        sub.subscribe_data_change(var)

    def positiveJog_Rot(self, AxisNo):
        Node = Axis[AxisNo - 1][0][1][0]
        Namespace = Axis[AxisNo - 1][0][1][1]
        Value = True
        self.writeBooleanValue(Node, Namespace, Value)
        # logging.debug("POSITIVE jog of rotatory axis:", AxisNo, ",NodeID: ns=", Namespace, ";i=", Node, ", Value:", Value)

    def negativeJog_Rot(self, AxisNo):
        Node = Axis[AxisNo - 1][0][0][0]
        Namespace = Axis[AxisNo - 1][0][0][1]
        Value = True
        self.writeBooleanValue(Node, Namespace, Value)
        # logging.debug("NEGATIVE jog of rotatory axis:", AxisNo, ",NodeID: ns=", Namespace, ";i=", Node, ", Value:", Value)

    def stopJog_Rot(self, AxisNo):
        Node1 = Axis[AxisNo - 1][0][0][0]
        Namespace1 = Axis[AxisNo - 1][0][0][1]
        Value1 = False
        Node2 = Axis[AxisNo - 1][0][1][0]
        Namespace2 = Axis[AxisNo - 1][0][1][1]
        Value2 = False
        self.writeBooleanValue(Node1, Namespace1, Value1)
        self.writeBooleanValue(Node2, Namespace2, Value2)
        # logging.debug("STOP jog of rotatory axis:", AxisNo)

    def positiveJog_Trans(self, AxisNo):
        Node = Axis[AxisNo - 1][1][1][0]
        Namespace = Axis[AxisNo - 1][1][1][1]
        Value = True
        self.writeBooleanValue(Node, Namespace, Value)
        # logging.debug("POSITIVE jog of translatory axis:", AxisNo, ",NodeID: ns=", Namespace, ";i=", Node, ", Value:", Value)

    def negativeJog_Trans(self, AxisNo):
        Node = Axis[AxisNo - 1][1][0][0]
        Namespace = Axis[AxisNo - 1][1][0][1]
        Value = True
        self.writeBooleanValue(Node, Namespace, Value)
        # logging.debug("NEGATIVE jog of translatory axis:", AxisNo, ",NodeID: ns=", Namespace, ";i=", Node, ", Value:", Value)

    def stopJog_Trans(self, AxisNo):
        Node1 = Axis[AxisNo - 1][1][0][0]
        Namespace1 = Axis[AxisNo - 1][1][0][1]
        Value1 = False
        Node2 = Axis[AxisNo - 1][1][1][0]
        Namespace2 = Axis[AxisNo - 1][1][1][1]
        Value2 = False
        self.writeBooleanValue(Node1, Namespace1, Value1)
        self.writeBooleanValue(Node2, Namespace2, Value2)
        # logging.debug("STOP jog of translatory axis:", AxisNo)

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
