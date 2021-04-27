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
