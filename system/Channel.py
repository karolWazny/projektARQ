from .Random import *
from .Packet import Packet


class Channel:
    def distort(self, packet):
        return packet


class StatelessChannel(Channel):
    """Klasa bazowa dla kanałów bezstanowych opartych na losowości."""

    def __init__(self, randomDevice=RandomizerImpl()):
        self.__randomizer = randomDevice
        self.__distortionProbabilityInPercent = 10

    def isBitDistorted(self):
        return self.__randomizer.getTrueWithProbability(percent=self.__distortionProbabilityInPercent)

    def setRandomizer(self, randDevice):
        self.__randomizer = randDevice

    def setChancesOfDistortingSingleBit(self, percentChance):
        self.__distortionProbabilityInPercent = percentChance


class BinarySymmetricChannel(StatelessChannel):
    """Kanał zaprzeczający dany bit z zadanym prawdopodobieństwem."""

    def __init__(self, randomDevice=RandomizerImpl()):
        super().__init__(randomDevice)

    def distort(self, packet):
        output = Packet()
        for bit in packet.content():
            output.add(bit=bool(bit) ^ bool(self.isBitDistorted()))
        return output


class BinaryErasureChannel(StatelessChannel):
    """Kanał zjadający dany bit z zadanym prawdopodobieństwem."""

    def __init__(self, randomDevice=RandomizerImpl()):
        super().__init__(randomDevice)

    def distort(self, packet):
        output = Packet()
        for bit in packet.content():
            if not self.isBitDistorted():
                output.add(bit)
        return output


class ZChannel(StatelessChannel):
    """Kanał zmieniający wartość bitu na 0 z zadanym prawdopodobieństwem."""

    def __init__(self, randomDevice=RandomizerImpl()):
        super().__init__(randomDevice)

    def distort(self, packet):
        output = Packet()
        for bit in packet.content():
            if self.isBitDistorted():
                output.add(False)
            else:
                output.add(bit)
        return output
