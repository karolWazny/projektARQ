from .Packet import Packet


class Transmitter:
    def __init__(self, encoder):
        self.encoder = encoder

    def transmit(self, packet):
        return self.encoder.encode(packet)

    @staticmethod
    def divSignal(signal, packetSize):
        packetList = []
        packet = Packet()
        for x in signal:
            packet.add(x)
            if packet.length() == packetSize:
                packetList.append(packet.content())
                packet.clear()
        return packetList




