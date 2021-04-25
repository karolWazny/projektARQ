import copy
from .Packet import Packet
import numpy as np
from Encoder import*
def xor(a,b):
    result = []
    for i in range(len(a)):
        sum=(a[i]+b[i])%2
        result.append(sum)
    return result

def div(divident, divisor):
    cDivident = 0
    result = []
    tmp = []
    length = len(divisor)
    cDivident = 0 #counter Divident
    while(sum(divident[0:(len(divident) - len(divisor) + 1)]) != 0):
        if(divident[cDivident]!=0):

            tmp = divident[cDivident:(cDivident+length)]
            result = xor(tmp,divisor)
            CResult=0 #counter Result
            while(length>CResult):
                divident[cDivident+CResult]=result[CResult]
                CResult += 1
        else:
            cDivident += 1

    return divident


class Decoder:
    def __init__(self):
        self.currentFrame = None
        self.receivedData = []
        self.key = []
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

    def decode(self):
        self.checkForErrors()
        return Packet

    def checkForErrors(self):
        self.currentFrame = div(self.currentFrame, self.key)
        if(sum(self.currentFrame)==0):
            pass
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
        self.aMatrix = np.full((self.__parityBits, self.__dataBits), 1)
        if self.__dataBits > 1:
            for rowIndex in range(self.__parityBits):
                self.aMatrix[rowIndex][rowIndex + 1] = 0

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
    def __init__(self,parameters):
        self.parameters = parameters

    def buildEncoder(self):
        return ParityEncoder

    def buildDecoder(self):
        return EvenDecoder

class CRCFactory:
    def __init__(self,parameters):
        self.parameters = parameters

    def buildEncoder(self):
        return CRCEncoder

    def buildDecoder(self):
        return CRCDecoder
if __name__ == '__main__':
    auto = HammingMatrixBuilder(5)
    print(auto.buildHMatrix())
    print(auto.buildGMatrix())

class DecoderException(Exception):
    """Wyjątek zgłaszany jako informacja o błędzie wykrytym w
    dekodowanym pakiecie."""

    def doSmth(self):
        return
