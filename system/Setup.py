from .Generator import Generator
from .Simulation import Simulation
from .TransmitterReceiverFactory import TransmitterFactory, ReceiverFactory
from .Channel import AllChannelFactory


class Setup:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog

    def run(self):
        generator = Generator(self.simulationLog.params.totalLength)
        channel = AllChannelFactory.buildFactory(self.simulationLog.params.noiseModel)
        transmitter = TransmitterFactory.createTransmitter(self.simulationLog.params.encoding,
                                                           self.simulationLog.params.crcKey,
                                                           self.simulationLog.params.hammingParityBits)
        receiver = ReceiverFactory.createReceiver(self.simulationLog.params.encoding, self.simulationLog.params.crcKey,
                                                  self.simulationLog.params.hammingParityBits)
        simulation = Simulation(generator, channel, transmitter, receiver, self.simulationLog)
        return simulation.simulate()
