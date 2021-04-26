from .Generator import Generator
from .Simulation import Simulation
from .ParametersAndOutput import SimulationParameters, SimulationLog, SimulationOutput
from .TransmitterReceiverFactory import TransmitterFactory, ReceiverFactory
from .Channel import ChannelFactoryFactory
from .Frontend import UserInteraction


class Setup:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog

    def run(self):
        generator = Generator(self.simulationLog.params.totalLength)
        channel = ChannelFactoryFactory.buildFactory(self.simulationLog.params.noiseModel)
        transmitter = TransmitterFactory.createTransmitter(self.simulationLog.params.encoding)
        receiver = ReceiverFactory.createReceiver(self.simulationLog.params.encoding)
        self.simulationLog.output = SimulationOutput()
        simulation = Simulation(generator, channel, transmitter, receiver, self.simulationLog)
        return simulation.simulate()
