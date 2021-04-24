from .Packet import Packet
import numpy

import copy
#https://www.geeksforgeeks.org/cyclic-redundancy-check-python/
def xor(a,b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return result

def mod2div(divident, divisor):
    divisorLenght = len(divisor)
    tmp = divident[0:divisorLenght]
    tmp2 = []
    for i in range(divisorLenght):
        tmp2.append(0)
    while divisorLenght < len(divident):
        if tmp[0] == 1:
            tmp3 = tmp
            tmp = xor(tmp3,divisor)
            tmp.append(divident[divisorLenght])
            tmp.append(0)
            divisorLenght += 1
        else:
            tmp3 = tmp
            tmp = xor(tmp3,tmp2)
            tmp.append(divident[divisorLenght])
            tmp.append(0)
            divisorLenght += 1
    if tmp[0] == 1:
        tmp3 = tmp
        tmp = xor(tmp3,divisor)
    else:
        tmp3 = tmp
        tmp = xor(tmp3,tmp2)
    tmp.pop[0]
    return tmp


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
            packet2=[]
            for element in packet:
                counter = 0;
                for bits in element:
                    if(bits=='1'):
                        counter += 1
                if(counter%2==1):
                    element += '1'
                else:
                    element += '0'
                packet2.append(element)
            packet = packet2
            return packet

class CRCEncoder(Encoder):
        def __init__(self):
            super().__init__()
        def encoder(self,packet):
            for element in packet:
                for i in range(len(self.key)-1):
                    packet[element].append(0)

                self.sentData = copy.deepcopy(self.data)
                self.sentData.extend(mod2div(packet[element], self.key))

            return packet