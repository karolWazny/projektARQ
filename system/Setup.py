from repo.system.Generator import Generator
from repo.system.Simulation import Simulation
from repo.system.TransmitterReceiverFactory import TransmitterReceiverFactory
from repo.system.Channel import AllChannelFactory


class Setup:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog

    def getSimulation(self):
        generator = Generator(self.simulationLog.params.totalLength)
        channel = AllChannelFactory.buildChannel(self.simulationLog.params.noiseModel)
        transmitterReceiverFactory = TransmitterReceiverFactory(self.simulationLog.params.encoding)
        transmitter = transmitterReceiverFactory.createTransmitter()
        receiver = transmitterReceiverFactory.createReceiver()
        simulation = Simulation(generator, channel, transmitter, receiver, self.simulationLog)
        return simulation
