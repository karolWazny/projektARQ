from .Generator import Generator
from .Simulation import Simulation
from .ParametersAndOutput import SimulationParameters, SimulationLog, SimulationOutput
from .TransmitterReceiverFactory import TransmitterFactory, ReceiverFactory
from .Channel import ChannelFactoryFactory


class Setup:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog

    def run(self):
        generator = Generator(self.simulationLog.params.totalLength)
        channel = ChannelFactoryFactory.buildFactory(self.simulationLog.params)
        transmitter = TransmitterFactory.createTransmitter(self.simulationLog.params.encoding)
        receiver = ReceiverFactory.createReceiver(self.simulationLog.params.encoding)
        self.simulationLog.output = SimulationOutput()
        simulation = Simulation(generator, channel, transmitter, receiver, self.simulationLog)
        return simulation.simulate()


class UserInteraction:

    @staticmethod
    def choiceParameters():
        simulationLog = SimulationLog()
        simParams = SimulationParameters()
        while simParams.packetLength is not None and simParams.totalLength is not None and simParams.encoding is not None and simParams.noiseModel is not None:
            try:
                simParams.totalLength = input("Podaj dlugosc ciagu do transmisji: ")
                if not type(simParams.totalLength) is int:
                    raise TypeError("Only integers are allowed")
                if simParams.totalLength < 0:
                    raise ValueError("Sorry, no numbers below zero")
                simParams.packetLength = input("Podaj dlugosc wysylanego pakietu")
                if not type(simParams.packetLength) is int:
                    raise TypeError("Only integers are allowed")
                if simParams.packetLength < 0:
                    raise ValueError("Sorry, no numbers below zero")
                simParams.noiseModel = input("Podaj rodzaj znieksztalcania")
                if not simParams.__eq__(simParams.noiseModel):
                    raise NameError("Only noiseModels from dictionary are allowed")
                simParams.encoding = input("Podaj rodzaj kodowania")
                if not simParams.__eq__(simParams.encoding):
                    raise NameError("Only codingModels from dictionary are allowed")
            except (TypeError, ValueError, NameError):
                pass
        simulationLog.params = simParams
        setup = Setup(simulationLog)
        return setup


class Main:
    if __name__ == '__main__':
        setup = UserInteraction.choiceParameters()
        simulationLog = setup.run()
