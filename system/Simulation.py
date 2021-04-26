from .Transmitter2 import Diver


class Simulation:
    def __init__(self, generator, channel, transmitter, receiver, simulationLog):
        self.generator = generator
        self.channel = channel
        self.transmitter = transmitter
        self.receiver = receiver
        self.simulationLog = simulationLog

    def simulate(self):
        signal = self.generator.generate()
        packetList = Diver.divSignal(signal, self.simulationLog.params.packetLength)
        for packet in packetList:
            receivedPacket = None
            while receivedPacket is None:
                self.simulationLog.output.transmissionsTotal += 1
                codedPacket = self.transmitter.transmit(packet)
                distortedPacket = self.channel.distort(codedPacket)
                receivedPacket = self.receiver.receive(distortedPacket)
                if receivedPacket is None:
                    self.simulationLog.output.retransmissions += 1
            if receivedPacket != packet:
                self.simulationLog.output.errorsUndetected += 1
        self.simulationLog.output.errorsTotal = self.simulationLog.output.errorsUndetected + self.simulationLog.output.retransmissions
        return self.simulationLog
