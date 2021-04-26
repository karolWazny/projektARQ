from .Generator import Generator
from .Simulation import Simulation
from .TransmitterReceiverFactory import TransmitterFactory, ReceiverFactory
from .Channel import ChannelFactoryFactory


class Setup:
    def __init__(self, simulationLog, key, parityBits):
        self.simulationLog = simulationLog
        self.key = key
        self.parityBits = parityBits

    def run(self):
        generator = Generator(self.simulationLog.params.totalLength)
        channel = ChannelFactoryFactory.buildFactory(self.simulationLog.params.noiseModel)
        transmitter = TransmitterFactory.createTransmitter(self.simulationLog.params.encoding, self.key, self.parityBits)
        receiver = ReceiverFactory.createReceiver(self.simulationLog.params.encoding, self.key, self.parityBits)
        simulation = Simulation(generator, channel, transmitter, receiver, self.simulationLog)
        return simulation.simulate()
