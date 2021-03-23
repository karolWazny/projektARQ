import Random
from Packet import Packet


class Distortion:
    def distort(self, packet):
        return packet


class SimpleDistortion(Distortion):
    def __init__(self, randomDevice=Random.RandomizerImpl):
        self.randomizer = randomDevice
        self.distortionProbabilityInPercent = 10

    def distort(self, packet):
        output = Packet(length=packet.length)
        for bit in packet.bits:
            output.addBit(bit=bool(bit) ^ bool(self.isBitDistorted()))
        return output

    def isBitDistorted(self):
        return self.randomizer.getBooleanWithProbability(percent=self.distortionProbabilityInPercent)

    def setRandomizer(self, randDevice):
        self.randomizer = randDevice
