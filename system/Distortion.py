from .Random import *
from .Packet import Packet


class Distortion:
    def distort(self, packet):
        return packet


class SimpleDistortion(Distortion):
    def __init__(self, randomDevice=RandomizerImpl()):
        self.__randomizer = randomDevice
        self.__distortionProbabilityInPercent = 10

    def distort(self, packet):
        output = Packet()
        for bit in packet.content():
            output.add(bit=bool(bit) ^ bool(self.isBitDistorted()))
        return output

    def isBitDistorted(self):
        return self.__randomizer.getTrueWithProbability(percent=self.__distortionProbabilityInPercent)

    def setRandomizer(self, randDevice):
        self.__randomizer = randDevice

    def setChancesOfDistortingSingleBit(self, percentChance):
        self.__distortionProbabilityInPercent = percentChance
