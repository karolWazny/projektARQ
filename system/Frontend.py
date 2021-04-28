import tkinter as tk
from repo.system.ParametersAndOutput import *
from repo.system.Enums import *
from repo.system.Setup import *
from datetime import datetime


# klasa przekazana w ręce Karola
class UserInteraction:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog

    def chooseParameters(self):
        while self.simulationLog.params.packetLength is not None or self.simulationLog.params.totalLength is not None \
                or self.simulationLog.params.encoding is not None or self.simulationLog.params.noiseModel is not None:
            try:
                self.simulationLog.params.totalLength = input("Podaj dlugosc ciagu do transmisji: ")
                if not type(self.simulationLog.params.totalLength) is int:
                    raise TypeError("Only integers are allowed")
                if self.simulationLog.params.totalLength < 0:
                    raise ValueError("Sorry, no numbers below zero")
                self.simulationLog.params.packetLength = input("Podaj dlugosc wysylanego pakietu")
                if not type(self.simulationLog.params.packetLength) is int:
                    raise TypeError("Only integers are allowed")
                if self.simulationLog.params.packetLength < 0:
                    raise ValueError("Sorry, no numbers below zero")
                self.simulationLog.params.noiseModel = input("Podaj rodzaj znieksztalcania")
                if not self.simulationLog.params.__eq__(self.simulationLog.params.noiseModel):
                    raise NameError("Only noiseModels from dictionary are allowed")
                self.simulationLog.params.encoding = input("Podaj rodzaj kodowania")
                if not self.simulationLog.params.__eq__(self.simulationLog.params.encoding):
                    raise NameError("Only codingModels from dictionary are allowed")
            except (TypeError, ValueError, NameError):
                pass
        return self.simulationLog


class Main:
    def __init__(self):
        self.window = self.prepareWindow()
        self.parameters = self.obtainParameters()

    def prepareWindow(self):
        window = tk.Tk(className="arq simulator")  # todo wymusic zaczynanie z wielkiej litery
        runButt = tk.Button(window, text="Run simulation", command=self.runSimulation)
        runButt.pack()
        paramButt = tk.Button(window, text="Change Parameters", command=self.changeParameters)
        paramButt.pack()
        window.geometry("250x100")
        return window

    def run(self):
        self.window.mainloop()

    def obtainParameters(self):
        try:
            params = readParametersFromJson('params.json')
        except FileNotFoundError:
            params = self.makeDefaultParameters()
            saveObjectToJson(params, 'params.json')
        return params

    def makeDefaultParameters(self):
        params = SimulationParameters()
        params.packetLength = 8
        params.totalLength = 1024
        params.noiseModel = {'type': Noise.BINARY_SYMMETRIC,
                             'BER': 10}
        params.encoding = {'type': Encoding.PARITY}
        return params

    def runSimulation(self):
        now = datetime.now()
        log = SimulationLog()
        log.params = self.parameters
        setup = Setup(log)
        simulation = setup.getSimulation()
        simulation.simulate()
        filename = now.strftime("%Y-%m-%d-%H%M%S")
        saveObjectToJson(log, filename)

    def changeParameters(self):
        pass

