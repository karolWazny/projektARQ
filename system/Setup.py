from repo.system.Generator import Generator
from repo.system.Simulation import Simulation
from repo.system.TransmitterReceiverFactory import TransmitterFactory, ReceiverFactory
from repo.system.Channel import AllChannelFactory


class Setup:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog

    def getSimulation(self):
        generator = Generator(self.simulationLog.params.totalLength)
        channel = AllChannelFactory.buildChannel(self.simulationLog.params.noiseModel)
        transmitter = TransmitterFactory.createTransmitter(self.simulationLog.params.encoding)
        receiver = ReceiverFactory.createReceiver(self.simulationLog.params.encoding)
        simulation = Simulation(generator, channel, transmitter, receiver, self.simulationLog)
        return simulation
