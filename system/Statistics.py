from numpy import mean
import matplotlib.pyplot as plt


class Avg:
    def __init__(self, simulationLog):
        self.simulationLog = simulationLog
        self.avgTransmissionsTotal = 0
        self.avgRetransmissions = 0
        self.avgErrorsTotal = 0
        self.avgErrorsUndetected = 0

    def calculate(self):
        transmissionsTotal = []
        retransmissions = []
        errorsTotal = []
        errorsUndetected = []
        for output in self.simulationLog.output:
            transmissionsTotal.append(output.transmissionsTotal)
            retransmissions.append(output.retransmissions)
            errorsTotal.append(output.errorsTotal)
            errorsUndetected.append(output.errorsUndetected)
        self.avgTransmissionsTotal = mean(transmissionsTotal)
        self.avgRetransmissions = mean(retransmissions)
        self.avgErrorsTotal = mean(errorsTotal)
        self.avgErrorsUndetected = mean(errorsUndetected)

    def showGraph(self):
        x = ["Liczba transmisji", "Liczba retransmisji", "Niewykryte błędy", "Wszystkie błędy"]
        y = [self.avgTransmissionsTotal, self.avgRetransmissions, self.avgErrorsUndetected, self.avgErrorsTotal]
        plt.bar(x, y)
        plt.show()


class SimulationLogTest:
    def __init__(self):
        self.output = []


class SimulationOutputTest:
    def __init__(self):
        self.transmissionsTotal = 0
        self.retransmissions = 0
        self.errorsTotal = 0
        self.errorsUndetected = 0


class Test:
    if __name__ == '__main__':
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

        avg = Avg(simLog)
        avg.calculate()
        avg.showGraph()

