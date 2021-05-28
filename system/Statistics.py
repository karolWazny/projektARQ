import pandas as pd
from numpy import mean
import statistics
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm


def normalDistrib(x, avg, s, amp):
    return norm.pdf(x, avg, s) * amp


class ParametricFit:
    def __init__(self, multipleRunLog):
        self.log = multipleRunLog

    def draw(self):
        packetErrorRatios = []
        for element in self.log.output:
            packetErrorRatios.append(element.errorsTotal / element.transmissionsTotal * 1000)
        y_values = []
        x_values = []
        for index in range(0, 1000, 1):
            x_values.append(index / 1000)
            inRange, left, right = 0, index - 25, index + 25
            for element in packetErrorRatios:
                inRange += (left < element) and (element < right)
            y_values.append(inRange)

        plt.plot(x_values, y_values)

        popt, pcov = curve_fit(normalDistrib, x_values, y_values)

        plt.plot(x_values, normalDistrib(x_values, *popt), 'r-',
                 label='fit: avg=%5.3f, sigm=%5.3f, amp=%5.3f' % tuple(popt))

        plt.xlabel('pakietowa stopa bledu')
        plt.ylabel('liczba wystapien na 10000 symulacji')
        plt.legend()
        plt.show()


class PrepareData:
    def __init__(self, multipleRunLog):
        self.multipleRunLog = multipleRunLog
        self.transmissionsTotal = []
        self.retransmissions = []
        self.errorsTotal = []
        self.errorsUndetected = []
        self.__makeUsefulData()

    def __makeUsefulData(self):
        for output in self.multipleRunLog.output:
            self.transmissionsTotal.append(output.transmissionsTotal)
            self.retransmissions.append(output.retransmissions)
            self.errorsTotal.append(output.errorsTotal)
            self.errorsUndetected.append(output.errorsUndetected)


class Avg:
    def __init__(self, usefulData):
        self.usefulData = usefulData
        self.avgTransmissionsTotal = 0
        self.avgRetransmissions = 0
        self.avgErrorsTotal = 0
        self.avgErrorsUndetected = 0
        self.calculate()

    def calculate(self):
        self.avgTransmissionsTotal = mean(self.usefulData.transmissionsTotal)
        self.avgRetransmissions = mean(self.usefulData.retransmissions)
        self.avgErrorsTotal = mean(self.usefulData.errorsTotal)
        self.avgErrorsUndetected = mean(self.usefulData.errorsUndetected)

    def showGraph(self):
        x = ["L. transmisji", "L. retransmisji", "Niewykryte błędy", "Wszystkie błędy"]
        y = [self.avgTransmissionsTotal, self.avgRetransmissions, self.avgErrorsUndetected, self.avgErrorsTotal]
        plt.figtext(0, 0, ' dlugosc sygnalu = ' + str(self.usefulData.multipleRunLog.params.totalLength) +
                 '\n dlugosc pakietu = ' + str(self.usefulData.multipleRunLog.params.packetLength) +
                 '\n rodzaj zaszumiania = ' + str(self.usefulData.multipleRunLog.params.noiseModel) +
                 '\n rodzaj kodowania = ' + str(self.usefulData.multipleRunLog.params.encoding))
        plt.subplot(2, 1, 1)
        plt.bar(x, y)
        plt.title("ŚREDNIA ARYTMETYCZNA " + str(len(self.usefulData.multipleRunLog.output)) + " PRÓB")
        plt.subplot(2, 1, 2)
        plt.pie(y, labels=x, startangle=90)
        plt.show()


class Histogram:
    def __init__(self, usefulData):
        self.usefulData = usefulData

    def showGraph(self):
        plt.suptitle("Histogram")
        plt.figtext(0, 0, ' dlugosc sygnalu = ' + str(self.usefulData.multipleRunLog.params.totalLength) +
                 '\n dlugosc pakietu = ' + str(self.usefulData.multipleRunLog.params.packetLength) +
                 '\n rodzaj zaszumiania = ' + str(self.usefulData.multipleRunLog.params.noiseModel) +
                 '\n rodzaj kodowania = ' + str(self.usefulData.multipleRunLog.params.encoding))
        plt.subplot(2, 2, 1)
        plt.hist(self.usefulData.transmissionsTotal)
        plt.title("L. wszystkich transmisji")
        plt.subplot(2, 2, 2)
        plt.hist(self.usefulData.retransmissions)
        plt.title("L. wszystkich retransmisji")
        plt.subplot(2, 2, 3)
        plt.hist(self.usefulData.errorsUndetected)
        plt.title("L. niewykrytych błędów")
        plt.subplot(2, 2, 4)
        plt.hist(self.usefulData.errorsTotal)
        plt.title("L. wszystkich błędów")
        plt.show()

class FiveNumberSummary:
    def __init__(self, usefulData):
        self.usefulData = usefulData
        self.usefulData = usefulData
        self.minTransmissionsTotal = 0
        self.minRetransmissions = 0
        self.minErrorsTotal = 0
        self.minErrorsUndetected = 0
        self.over25TransmissionsTotal = 0
        self.over25Retransmissions = 0
        self.over25ErrorsTotal = 0
        self.over25ErrorsUndetected = 0
        self.medianTransmissionsTotal = 0
        self.medianRetransmissions = 0
        self.medianErrorsTotal = 0
        self.medianErrorsUndetected = 0
        self.over75TransmissionsTotal = 0
        self.over75Retransmissions = 0
        self.over75ErrorsTotal = 0
        self.over75ErrorsUndetected = 0
        self.maxTransmissionsTotal = 0
        self.maxRetransmissions = 0
        self.maxErrorsTotal = 0
        self.maxErrorsUndetected = 0

    def showBoxplot(self):
        df = pd.DataFrame({'TransmissionsTotal' : self.usefulData.transmissionsTotal,
                                'Retransmissions' : self.usefulData.retransmissions,
                                'ErrorsTotal' : self.usefulData.errorsTotal,
                                'ErrorsUndetected' : self.usefulData.errorsUndetected})

        self.minTransmissionsTotal = min(self.usefulData.transmissionsTotal)
        self.minRetransmissions = min(self.usefulData.retransmissions)
        self.minErrorsTotal = min(self.usefulData.errorsTotal)
        self.minErrorsUndetected = min(self.usefulData.errorsUndetected)
        self.over25TransmissionsTotal = df['TransmissionsTotal'].quantile([0.25])
        self.over25Retransmissions = df['Retransmissions'].quantile([0.25])
        self.over25ErrorsTotal = df['ErrorsTotal'].quantile([0.25])
        self.over25ErrorsUndetected = df['ErrorsUndetected'].quantile([0.25])
        self.medianTransmissionsTotal = df['TransmissionsTotal'].quantile([0.5])
        self.medianRetransmissions = df['Retransmissions'].quantile([0.5])
        self.medianErrorsTotal = df['ErrorsTotal'].quantile([0.5])
        self.medianErrorsUndetected = df['ErrorsUndetected'].quantile([0.5])
        self.over75TransmissionsTotal = df['TransmissionsTotal'].quantile([0.75])
        self.over75Retransmissions = df['Retransmissions'].quantile([0.75])
        self.over75ErrorsTotal = df['ErrorsTotal'].quantile([0.75])
        self.over75ErrorsUndetected = df['ErrorsUndetected'].quantile([0.75])
        self.maxTransmissionsTotal = max(self.usefulData.transmissionsTotal)
        self.maxRetransmissions = max(self.usefulData.retransmissions)
        self.maxErrorsTotal = max(self.usefulData.errorsTotal)
        self.maxErrorsUndetected = max(self.usefulData.errorsUndetected)


        plt.title("Wykres pudełkowy")
        boxplot = df.boxplot(column = ['TransmissionsTotal','Retransmissions','ErrorsTotal','ErrorsUndetected'])
        plt.show()

# odtąd są testy działania statystyk
class MultipleRunLogTest:
    def __init__(self):
        self.output = []
        self.params = SimulationParametersTest()


class SimulationParametersTest:
    def __init__(self):  # tylko do sprawdzenia czy się wyświetlają te wartości na wykresach
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
        simLog = MultipleRunLogTest()
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


if __name__ == '__main__':
    multipleRunLog = RandomOutputs.generateRandomOutputs()
    preparedLists = PrepareData(multipleRunLog)
    preparedLists.makeUsefulData()
    avg = Avg(preparedLists)
    avg.calculate()
    avg.showGraph()
    hist = Histogram(preparedLists)
    hist.showGraph()
    boxplot = FiveNumberSummary(preparedLists)
    boxplot.showBoxplot()
