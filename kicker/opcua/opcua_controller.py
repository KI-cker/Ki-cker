import logging

from kicker.opcua.opcua_base import OpcuaBase
from opcua import ua

from kicker.opcua.opcua_constants import PosMode_Ack_Rot_Tor, PosMode_Ack_Rot_Verteidiung, PosMode_Ack_Rot_Mittelfeld, \
    PosMode_Ack_Rot_Sturm, PosMode_Ack_Trans_Tor, PosMode_Ack_Trans_Verteidiung, PosMode_Ack_Trans_Mittelfeld, \
    PosMode_Ack_Trans_Sturm, Axis, startEmulation


class OpcuaController(OpcuaBase):
    def __init__(self):
        super(OpcuaController, self).__init__()

    def resetEmulation(self, value=True):
        var = self.client.get_node(
            ua.NodeId(startEmulation[0], startEmulation[1]))
        var.set_value(ua.Variant(value, ua.VariantType.Boolean))

    def connect(self):
        self.client.connect()
        root = self.client.get_root_node()
        if (root != ""):
            logging.info("Connection established")
            ack_axis1 = self.readValue_polling(
                PosMode_Ack_Rot_Tor[0], PosMode_Ack_Rot_Tor[1])
            ack_axis2 = self.readValue_polling(
                PosMode_Ack_Rot_Verteidiung[0], PosMode_Ack_Rot_Verteidiung[1])
            ack_axis3 = self.readValue_polling(
                PosMode_Ack_Rot_Mittelfeld[0], PosMode_Ack_Rot_Mittelfeld[1])
            ack_axis4 = self.readValue_polling(
                PosMode_Ack_Rot_Sturm[0], PosMode_Ack_Rot_Sturm[1])
            ack_axis5 = self.readValue_polling(
                PosMode_Ack_Trans_Tor[0], PosMode_Ack_Trans_Tor[1])
            ack_axis6 = self.readValue_polling(
                PosMode_Ack_Trans_Verteidiung[0], PosMode_Ack_Trans_Verteidiung[1])
            ack_axis7 = self.readValue_polling(
                PosMode_Ack_Trans_Mittelfeld[0], PosMode_Ack_Trans_Mittelfeld[1])
            ack_axis8 = self.readValue_polling(
                PosMode_Ack_Trans_Sturm[0], PosMode_Ack_Trans_Sturm[1])
            initDone = ack_axis1 and ack_axis2 and ack_axis3 and ack_axis4 and ack_axis5 and ack_axis6 and ack_axis7 and ack_axis8

            if (initDone != True):
                logging.info("axis not ready yet or error")

            if (initDone == True):
                logging.info("axis ready")
        else:
            logging.info("Could not connect to server!")

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
