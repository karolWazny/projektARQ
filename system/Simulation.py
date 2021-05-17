from .ParametersAndOutput import SimulationOutput


class Simulation:
    def __init__(self, generator, channel, transmitter, receiver, simulationLog):
        self.generator = generator
        self.channel = channel
        self.transmitter = transmitter
        self.receiver = receiver
        self.simulationLog = simulationLog

    def simulate(self):
        signal = self.generator.generate()
        packetList = self.transmitter.divSignal(signal, self.simulationLog.params.packetLength)
        for packet in packetList:
            receivedPacket = None
            singlePacketRetransmissions = 0
            while receivedPacket is None:
                self.simulationLog.output.transmissionsTotal += 1
                codedPacket = self.transmitter.transmit(packet)
                distortedPacket = self.channel.distort(codedPacket)
                receivedPacket = self.receiver.receive(distortedPacket)
                if receivedPacket is None:
                    self.simulationLog.output.retransmissions += 1
                    singlePacketRetransmissions += 1
                if singlePacketRetransmissions >= 100:
                    raise Exception
            if receivedPacket != packet:
                self.simulationLog.output.errorsUndetected += 1
        self.simulationLog.output.errorsTotal = self.simulationLog.output.errorsUndetected + self.simulationLog.output.retransmissions
        return self.simulationLog

    def reset(self):
        self.simulationLog.output = SimulationOutput()
