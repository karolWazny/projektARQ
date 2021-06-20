import copy
import numpy as np

from .Encoder import HammingEncoder, ParityEncoder, CRCEncoder
from .Packet import Packet


def xor(a, b):
    result = []
    for i in range(len(a)):
        sum = (a[i] + b[i]) % 2
        result.append(sum)
    return result


def div(divident, divisor):
    cDivident = 0
    result = []
    tmp = []
    length = len(divisor)
    cDivident = 0  # counter Divident
    while sum(divident[0:(len(divident) - len(divisor) + 1)]) != 0:
        if divident[cDivident] != 0:

            tmp = divident[cDivident:(cDivident + length)]
            result = xor(tmp, divisor)
            CResult = 0  # counter Result
            while length > CResult:
                divident[cDivident + CResult] = result[CResult]
                CResult += 1
        else:
            cDivident += 1

    return divident


class Decoder:
    def __init__(self):
        self.currentFrame = None
        self.retransmission = False

    def passFrame(self, packet):
        self.currentFrame = packet

    def decode(self):
        return self.currentFrame


class ParityDecoder(Decoder):
    def decode(self):
        self.checkForError()
        return self.makeOutput()

    def checkForError(self):
        if self.isOdd() or self.isEmpty():
            raise DecoderException

    def makeOutput(self):
        output = Packet()
        for bit in self.currentFrame.content():
            output.add(bit)
        output.content().pop(-1)
        return output

    def isEmpty(self):
        return self.currentFrame.length() == 0

    def isOdd(self):
        isOdd = sum(self.currentFrame.content()) % 2
        return isOdd


class HammingDecoder(Decoder):
    def __init__(self, matrixBuilder):
        self.hTransposedMatrix = matrixBuilder.buildHMatrix().transpose()
        self.k = matrixBuilder.getDataBits()

    def decode(self):
        self.checkForErrors()
        return self.buildOutput()

    def checkForErrors(self):
        if self.currentFrame.length() != len(self.hTransposedMatrix):
            raise DecoderException
        errorMatrix = np.dot(self.currentFrame.content(), self.hTransposedMatrix)
        for value in errorMatrix:
            value &= 0x1
            if value == 1:
                raise DecoderException

    def buildOutput(self):
        return Packet.fromList(self.currentFrame.content()[0: self.k])


class CRCDecoder(Decoder):
    def __init__(self, key):
        self.key = key

    def decode(self):
        return self.checkForErrors()

    def checkForErrors(self):
        tmp = copy.deepcopy(self.currentFrame.content())
        decodedPacket = div(tmp, self.key)
        if sum(decodedPacket) == 0:
            return Packet.fromList(self.currentFrame.content()[:-len(self.key) + 1])
        else:
            raise DecoderException


class HammingMatrixBuilder:
    def __init__(self, m=3):
        self.__parityBits = m
        self.__totalBits = self.calculateTotalBits()
        self.__dataBits = self.calculateDataBits()
        self.aMatrix = None
        self.buildAMatrix()

    def calculateDataBits(self):
        return self.__totalBits - self.__parityBits

    def calculateTotalBits(self):
        return 2 ** self.__parityBits - 1

    def buildHMatrix(self):
        return np.append(self.aMatrix, np.identity(self.__totalBits - self.__dataBits, dtype=int), axis=1)

    def buildGMatrix(self):
        return np.append(np.identity(self.__dataBits, dtype=int), self.aMatrix.transpose(), axis=1)

    def buildAMatrix(self):
        columnIndex, self.aMatrix = 0, np.empty((self.__parityBits, 0), dtype=bool)
        for index in range(3, 2 ** self.__parityBits):
            row, count, num = np.empty((self.__parityBits, 1), dtype=bool), 0, 1
            for j in range(0, self.__parityBits):
                tmp = index & num
                if tmp != 0:
                    count += 1
                    row[j][0] = 1
                else:
                    row[j][0] = 0
                num = num << 1
            if count > 1:
                self.aMatrix = np.append(self.aMatrix, row, axis=1)

    def getDataBits(self):
        return self.__dataBits


class HammingFactory:
    def __init__(self, parameters):
        self.parameters = parameters
        self.matrixBuilder = HammingMatrixBuilder(parameters['parityBits'])

    def buildEncoder(self):
        return HammingEncoder(self.matrixBuilder)

    def buildDecoder(self):
        return HammingDecoder(self.matrixBuilder)


class ParityFactory:
    @staticmethod
    def buildEncoder():
        return ParityEncoder()

    @staticmethod
    def buildDecoder():
        return ParityDecoder()


class CRCFactory:
    def __init__(self, key):
        self.parameters = key

    def buildEncoder(self):
        return CRCEncoder(self.parameters)

    def buildDecoder(self):
        return CRCDecoder(self.parameters)


if __name__ == '__main__':
    auto = HammingMatrixBuilder(5)
    print(auto.buildHMatrix())
    print(auto.buildGMatrix())


class DecoderException(Exception):
    """Wyjątek zgłaszany jako informacja o błędzie wykrytym w
    dekodowanym pakiecie."""

    def doSmth(self):
        return
