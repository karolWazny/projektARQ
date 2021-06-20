import pandas as pd
from numpy import mean
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm
import random


def normalDistrib(x, avg, s, amp):
    return norm.pdf(x, avg, s) * amp


class ParametricFit:
    def __init__(self, multipleRunLog):
        self.ratios = []
        self.log = multipleRunLog

    def drawDamagedPacketsRatioDistrib(self):
        self.ratios = []
        for element in self.log.output:
            self.ratios.append(element.errorsTotal / element.transmissionsTotal * 1000)
        self.__draw('pakietowa stopa bledu')

    def drawUndetectedToTotalErrorsRatioDistrib(self):
        self.ratios = []
        for element in self.log.output:
            self.ratios.append(element.errorsUndetected / element.errorsTotal * 1000)
        self.__draw('stosunek bledow niewykrytych do wszystkich bledow')

    def __draw(self, xlabel):
        y_values = []
        x_values = []
        for index in range(0, 1000, 1):
            x_values.append(index / 1000)
            inRange, left, right = 0, index - 0.5, index + 0.5
            for element in self.ratios:
                inRange += (left < element) and (element < right)
            y_values.append(inRange)

        plt.plot(x_values, y_values)

        popt, pcov = curve_fit(normalDistrib, x_values, y_values)

        plt.plot(x_values, normalDistrib(x_values, *popt), 'r-',
                 label='fit: avg=%5.3f, sigm=%5.3f, amp=%5.3f' % tuple(popt))

        plt.xlabel(xlabel)
        plt.ylabel('liczba wystapien na 10000 symulacji')
        plt.legend()
        plt.show()


class PrepareData:
    def __init__(self, multipleRunLog):
        self.multipleRunLog = multipleRunLog
        self.transmissionsTotal = list()
        self.retransmissions = list()
        self.errorsTotal = list()
        self.errorsUndetected = list()
        self.makeUsefulData()

    def makeUsefulData(self):
        for output in self.multipleRunLog.output:
            self.transmissionsTotal.append(output.transmissionsTotal)
            self.retransmissions.append(output.retransmissions)
            self.errorsTotal.append(output.errorsTotal)
            self.errorsUndetected.append(output.errorsUndetected)


class Avg(PrepareData):
    def __init__(self, multipleRunLog):
        super().__init__(multipleRunLog)
        self.avgErrorsUndetected = mean(self.errorsUndetected)
        self.avgErrorsTotal = mean(self.errorsTotal)
        self.avgRetransmissions = mean(self.retransmissions)
        self.avgTransmissionsTotal = mean(self.transmissionsTotal)

    def show(self):
        plt.figure(figsize=(8, 5))
        x = ["L. transmisji: " + str(round(self.avgTransmissionsTotal)),
             "L. retransmisji " + str(round(self.avgRetransmissions)),
             "Niewykryte błędy " + str(round(self.avgErrorsUndetected)),
             "Wszystkie błędy " + str(round(self.avgErrorsTotal))]
        y = [self.avgTransmissionsTotal, self.avgRetransmissions, self.avgErrorsUndetected, self.avgErrorsTotal]
        plt.figtext(0, 0, ' dlugosc sygnalu = ' + str(self.multipleRunLog.params.totalLength) +
                    '\n dlugosc pakietu = ' + str(self.multipleRunLog.params.packetLength) +
                    '\n rodzaj zaszumiania = ' + str(self.multipleRunLog.params.noiseModel) +
                    '\n rodzaj kodowania = ' + str(self.multipleRunLog.params.encoding))
        plt.subplot(2, 1, 1)
        plt.bar(x, y)
        plt.title("ŚREDNIA ARYTMETYCZNA " + str(len(self.multipleRunLog.output)) + " PRÓB")
        plt.subplot(2, 1, 2)
        x2 = ["L. wysłanych poprawnie " + str(round(self.avgTransmissionsTotal - self.avgErrorsTotal)),
              "L. wszystkich błędów " + str(round(self.avgErrorsTotal))]
        y2 = [self.avgTransmissionsTotal - self.avgErrorsTotal, self.avgErrorsTotal]
        plt.pie(y2, labels=x2, startangle=90)
        plt.show()


class Histogram(PrepareData):
    def __init__(self, multipleRunLog):
        super().__init__(multipleRunLog)

    def show(self):
        plt.figure(figsize=(10, 7.125))
        plt.suptitle("Histogram")
        plt.figtext(0, 0, ' dlugosc sygnalu = ' + str(self.multipleRunLog.params.totalLength) +
                    '\n dlugosc pakietu = ' + str(self.multipleRunLog.params.packetLength) +
                    '\n rodzaj zaszumiania = ' + str(self.multipleRunLog.params.noiseModel) +
                    '\n rodzaj kodowania = ' + str(self.multipleRunLog.params.encoding))
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


class FiveNumberSummary(PrepareData):
    def __init__(self, multipleRunLog):
        super().__init__(multipleRunLog)

    def showBoxplot(self):
        df = pd.DataFrame({'TransmissionsTotal': self.transmissionsTotal,
                           'Retransmissions': self.retransmissions,
                           'ErrorsTotal': self.errorsTotal,
                           'ErrorsUndetected': self.errorsUndetected})
        df['TransmissionsTotal'].quantile([0.25])
        df['Retransmissions'].quantile([0.25])
        df['ErrorsTotal'].quantile([0.25])
        df['ErrorsUndetected'].quantile([0.25])
        df['TransmissionsTotal'].quantile([0.5])
        df['Retransmissions'].quantile([0.5])
        df['ErrorsTotal'].quantile([0.5])
        df['ErrorsUndetected'].quantile([0.5])
        df['TransmissionsTotal'].quantile([0.75])
        df['Retransmissions'].quantile([0.75])
        df['ErrorsTotal'].quantile([0.75])
        df['ErrorsUndetected'].quantile([0.75])

        plt.title("Wykres pudełkowy")
        df.boxplot(column=['TransmissionsTotal', 'Retransmissions', 'ErrorsTotal', 'ErrorsUndetected'])
        plt.show()


# odtąd są testy działania statystyk (tylko do sprawdzenia czy się wyświetlają te wartości na wykresach)
class MultipleRunLogTest:
    def __init__(self):
        self.output = list()
        self.params = SimulationParametersTest()


class SimulationParametersTest:
    def __init__(self):
        self.totalLength = 125
        self.packetLength = 8
        self.noiseModel = "BINARY_SIMETRIC"
        self.encoding = "PARITY"


class SimulationOutputTest:
    def __init__(self):
        self.transmissionsTotal = 0
        self.retransmissions = 0
        self.errorsTotal = 0
        self.errorsUndetected = 0


class RandomOutputs:
    @staticmethod
    def generateRandomOutputs():
        multipleRunLogTest = MultipleRunLogTest()
        for i in range(100):
            simulationOutputTest = SimulationOutputTest()
            simulationOutputTest.retransmissions = random.randint(1, 300)
            simulationOutputTest.errorsUndetected = random.randint(1, 100)
            simulationOutputTest.transmissionsTotal = simulationOutputTest.retransmissions + \
                                                      simulationOutputTest.errorsUndetected + \
                                                      random.randint(1, 500)
            simulationOutputTest.errorsTotal = simulationOutputTest.errorsUndetected + simulationOutputTest.retransmissions
            multipleRunLogTest.output.append(simulationOutputTest)
        return multipleRunLogTest


if __name__ == '__main__':
    multipleRunLog = RandomOutputs.generateRandomOutputs()
    avg = Avg(multipleRunLog)
    avg.show()
    hist = Histogram(multipleRunLog)
    hist.show()
    boxplot = FiveNumberSummary(multipleRunLog)
    boxplot.showBoxplot()
