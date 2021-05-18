from numpy import mean
import matplotlib.pyplot as plt


class ParametricFit:
    pass


class Avg:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog
        self.avgTransmissionsTotal = 0
        self.avgRetransmissions = 0
        self.avgErrorsTotal = 0
        self.avgErrorsUndetected = 0
        self.simulationLog = simulationLog
        self.transmissionsTotal = []
        self.retransmissions = []
        self.errorsTotal = []
        self.errorsUndetected = []

    def calculate(self):
        for output in self.simulationLog.output:
            self.transmissionsTotal.append(output.transmissionsTotal)
            self.retransmissions.append(output.retransmissions)
            self.errorsTotal.append(output.errorsTotal)
            self.errorsUndetected.append(output.errorsUndetected)
        self.avgTransmissionsTotal = mean(self.transmissionsTotal)
        self.avgRetransmissions = mean(self.retransmissions)
        self.avgErrorsTotal = mean(self.errorsTotal)
        self.avgErrorsUndetected = mean(self.errorsUndetected)

    def showGraph(self):
        x = ["L. transmisji", "L. retransmisji", "Niewykryte błędy", "Wszystkie błędy"]
        y = [self.avgTransmissionsTotal, self.avgRetransmissions, self.avgErrorsUndetected, self.avgErrorsTotal]
        plt.subplot(2, 1, 1)
        plt.bar(x, y)
        plt.title("ŚREDNIA ARYTMETYCZNA " + str(len(self.simulationLog.output)) + " PRÓB")
        plt.subplot(2, 1, 2)
        plt.pie(y, labels=x, startangle=90)
        plt.show()


class Histogram:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog
        self.transmissionsTotal = []
        self.retransmissions = []
        self.errorsTotal = []
        self.errorsUndetected = []

    def calculate(self):
        for output in self.simulationLog.output:
            self.transmissionsTotal.append(output.transmissionsTotal)
            self.retransmissions.append(output.retransmissions)
            self.errorsTotal.append(output.errorsTotal)
            self.errorsUndetected.append(output.errorsUndetected)

    def showGraph(self):
        plt.subplot(2, 2, 1)
        plt.hist(self.transmissionsTotal)
        plt.title("L. wszystkich transmisji")
        plt.subplot(2, 2, 2)
        plt.hist(self.retransmissions)
        plt.title("L. wszystkich retransmisji")
        plt.subplot(2, 2, 3)
        plt.hist(self.errorsUndetected)
        plt.title("L. niewykrytych błędów")
        plt.subplot(2, 2, 4)
        plt.hist(self.errorsTotal)
        plt.title("L. wszystkich błędów")
        plt.show()


# odtąd są testy działania statystyk
class SimulationLogTest:
    def __init__(self):
        self.output = []


class SimulationOutputTest:
    def __init__(self):
        self.transmissionsTotal = 0
        self.retransmissions = 0
        self.errorsTotal = 0
        self.errorsUndetected = 0


class RandomOutputs:
    @staticmethod
    def generateRandomOutputs():
        simLog = SimulationLogTest()
        out1 = SimulationOutputTest()
        out1.transmissionsTotal = 12
        out1.retransmissions = 7
        out1.errorsUndetected = 2
        out1.errorsTotal = 9
        simLog.output.append(out1)

        out2 = SimulationOutputTest()
        out2.transmissionsTotal = 80
        out2.retransmissions = 25
        out2.errorsUndetected = 9
        out2.errorsTotal = 34
        simLog.output.append(out2)

        out3 = SimulationOutputTest()
        out3.transmissionsTotal = 69
        out3.retransmissions = 15
        out3.errorsUndetected = 3
        out3.errorsTotal = 18
        simLog.output.append(out3)

        out4 = SimulationOutputTest()
        out4.transmissionsTotal = 420
        out4.retransmissions = 123
        out4.errorsUndetected = 34
        out4.errorsTotal = 157
        simLog.output.append(out4)

        return simLog


class Test:
    if __name__ == '__main__':
        simulationLog = RandomOutputs.generateRandomOutputs()
        avg = Avg(simulationLog)
        avg.calculate()
        avg.showGraph()
        hist = Histogram(simulationLog)
        hist.calculate()
        hist.showGraph()
