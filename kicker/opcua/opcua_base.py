from opcua import ua
from opcua import Client

from kicker.opcua.opcua_constants import Axis, SubScriptionHandler

class OpcuaBase(object):
    def __init__(self):
        # self.client = Client("opc.tcp://100.102.7.5:4840")
        self.client = Client("opc.tcp://192.168.42.20:4840")

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
