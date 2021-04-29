import numpy

from repo.system.Packet import Packet
import copy


def CRCKey(packet, key):
    for i in range(len(key) - 1):
        packet.add(0)
    return packet


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


class Encoder:
    def __init__(self):
        self.currentPacket = None

    def encode(self, packet):
        self.currentPacket = packet
        return packet


class HammingEncoder(Encoder):
    def __init__(self, matrixBuilder):
        super().__init__()
        self.gMatrix = matrixBuilder.buildGMatrix()

    def encode(self, packet):
        content = numpy.dot(packet.content(), self.gMatrix)
        for index in range(0, len(content)):
            content[index] = content[index] % 2
        return Packet.fromList(content)


class ParityEncoder(Encoder):
    def __init__(self):
        super().__init__()

    def encode(self, packet):
        tmp = copy.deepcopy(packet.content())
        if sum(tmp) % 2 == 0:
            tmp.append(0)
        else:
            tmp.append(1)
        return Packet.fromList(tmp)


class CRCEncoder(Encoder):
    def __init__(self, key):
        self.key = key
        super().__init__()

    def encode(self, packet):
        tmp = copy.deepcopy(packet)
        tmp = CRCKey(tmp, self.key)
        tmp = div(tmp.content(), self.key)
        return Packet.fromList(tmp)
