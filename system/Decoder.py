import copy
from .Packet import Packet
import numpy as np
from Encoder import xor
from Encoder import mod2div


class Decoder:
    def __init__(self):
        self.currentFrame = None
        self.receivedData = []
        self.key = [0]
        self.retransmission = False

    def passFrame(self, packet):
        self.currentFrame = packet

    def decode(self):
        return self.currentFrame


class EvenDecoder(Decoder):
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
        isOdd = False
        for bit in self.currentFrame.content():
            isOdd = bool(isOdd) ^ bool(bit)
        return isOdd


class HammingDecoder(Decoder):
    def __init__(self, matrixBuilder):
        super().__init__()
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
    def passFrame(self, packet):
        for element in packet:
            isCorrect = True
            copyFrame = []
            decode = mod2div(self.receivedData, self.key)
            checksum = copy.copy(decode)
            for i in range(len(checksum)):
                if checksum[i] != 0:
                    isCorrect = False
                    break
            if isCorrect:
                self.retransmission = True
            else:
                self.retransmission = False
            self.retransmission(packet[element])
            checksum.clear()
            decode.clear()


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
        self.aMatrix = np.full((self.__parityBits, self.__dataBits), 1)
        if self.__dataBits > 1:
            for rowIndex in range(self.__parityBits):
                self.aMatrix[rowIndex][rowIndex + 1] = 0

    def getDataBits(self):
        return self.__dataBits


if __name__ == '__main__':
    auto = HammingMatrixBuilder(5)
    print(auto.buildHMatrix())
    print(auto.buildGMatrix())


class DecoderException(Exception):
    """Wyjątek zgłaszany jako informacja o błędzie wykrytym w
    dekodowanym pakiecie."""

    def doSmth(self):
        return
