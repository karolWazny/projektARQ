import numpy

from .Packet import Packet


class Encoder:
    def __init__(self):
        self.currentPacket = None

    def encode(self, packet):
        self.currentPacket = packet
        return packet


class HammingEncoder(Encoder):
    def __init__(self, matrixBuilder):
        super().__init__()
        self.gMatrix = matrixBuilder.buildGMatrix()

    def encode(self, packet):
        return Packet.fromList(numpy.dot(packet.content(), self.gMatrix))
