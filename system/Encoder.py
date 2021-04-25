from Packet import Packet
import copy
import numpy

def CRCKey(packet, key):
    for i in range(len(key)-1):
        packet.append(0)
    return packet

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

class Encoder:
    def __init__(self):
        self.currentPacket = None
        self.data = []
        self.sentData = []
        self.key = [0]


    def encode(self, packet):
        self.currentPacket = packet
        return packet


class HammingEncoder(Encoder):
    def __init__(self, matrixBuilder):
        super().__init__()
        self.gMatrix = matrixBuilder.buildGMatrix()


    def encode(self, packet):
        return Packet.fromList(numpy.dot(packet.content(), self.gMatrix))

class ParityEncoder(Encoder):
        def __init__(self):
            super().__init__()

        def encode(self,packet):
            packetParity = copy.deepcopy(packet)
            if sum(packetParity)%2 ==0:
                packetParity.append(0)
            else:
                packetParity.append(1)
            return packetParity

class CRCEncoder(Encoder):
        def __init__(self):
            super().__init__()

        def encode(self,packet,key):
            packetCRC = copy.deepcopy(packet)
            packetCRC =CRCKey(packetCRC,key)
            packetCRC=div(packetCRC,key)
            return packetCRC
