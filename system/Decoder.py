from Packet import Packet
import numpy as np


class Decoder:
    def __init__(self):
        self.currentFrame = None

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


class HammingDecoder(Decoder): #na ten moment tylko Hamming [7,4]
    def __init__(self, matrixBuilder):
        self.hMatrix = matrixBuilder.buildHMatrix()


class HammingMatrixBuilder:
    def __init__(self, m=3):
        self.__m = m
        self.__n = self.calculateN()
        self.__k = self.calculateK()
        self.aMatrix = None
        self.buildAMatrix()

    def calculateK(self):
        return self.__n - self.__m

    def calculateN(self):
        return 2 ** self.__m - 1

    def buildHMatrix(self):
        return np.append(self.aMatrix, np.identity(self.__n - self.__k, dtype=int), axis=1)

    def buildGMatrix(self):
        return np.append(np.identity(self.__k, dtype=int), self.aMatrix.transpose(), axis=1)

    def buildAMatrix(self):
        self.aMatrix = np.identity(self.__n - self.__k, dtype=int)
        self.aMatrix = np.logical_not(self.aMatrix)
        self.aMatrix = np.flipud(self.aMatrix)
        column = np.full((self.__n - self.__k, 1), 1)
        self.aMatrix = np.append(self.aMatrix, column, axis=1)



class DecoderException(Exception):
    """Wyjątek zgłaszany jako informacja o błędzie wykrytym w
    dekodowanym pakiecie."""

    def doSmth(self):
        return
