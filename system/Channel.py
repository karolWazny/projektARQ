from .Enums import Noise
from .Packet import Packet
from .Random import RandomizerImpl


class Channel:
    def distort(self, packet):
        return packet


class StatelessChannel(Channel):
    """Klasa bazowa dla kanałów bezstanowych opartych na losowości."""

    def __init__(self, BER, randomDevice):
        self.__randomizer = randomDevice
        self.__distortionProbabilityInPercent = BER

    def isBitDistorted(self):
        return self.__randomizer.getTrueWithProbability(percent=self.__distortionProbabilityInPercent)

    def setRandomizer(self, randDevice):
        self.__randomizer = randDevice

    def setChancesOfDistortingSingleBit(self, percentChance):
        self.__distortionProbabilityInPercent = percentChance


# https://en.wikipedia.org/wiki/Binary_symmetric_channel
class BinarySymmetricChannel(StatelessChannel):
    """Kanał zaprzeczający dany bit z zadanym prawdopodobieństwem."""

    def __init__(self, BER=10, randomDevice=RandomizerImpl()):
        super().__init__(BER, randomDevice)
        self.setChancesOfDistortingSingleBit(BER)

    def distort(self, packet):
        output = Packet()
        for bit in packet.content():
            output.add(bit=bool(bit) ^ bool(self.isBitDistorted()))
        return output


# https://en.wikipedia.org/wiki/Binary_erasure_channel#Related_channels
class BinaryErasureChannel(StatelessChannel):
    """Kanał zjadający dany bit z zadanym prawdopodobieństwem."""

    def __init__(self, BER=10, randomDevice=RandomizerImpl()):
        super().__init__(BER, randomDevice)

    def distort(self, packet):
        output = Packet()
        for bit in packet.content():
            if not self.isBitDistorted():
                output.add(bit)
        return output


# https://en.wikipedia.org/wiki/Z-channel_(information_theory)
class ZChannel(StatelessChannel):
    """Kanał zmieniający wartość bitu na 0 z zadanym prawdopodobieństwem."""

    def __init__(self, BER=10, randomDevice=RandomizerImpl()):
        super().__init__(BER, randomDevice)

    def distort(self, packet):
        output = Packet()
        for bit in packet.content():
            if self.isBitDistorted():
                output.add(False)
            else:
                output.add(bit)
        return output


# https://core.ac.uk/download/pdf/187610741.pdf
class DefiniteStateMarkovChannel(Channel):
    def __init__(self):
        return


class TwoStateMarkovChannel(Channel):
    def __init__(self, stateOneChannel=BinarySymmetricChannel(10), stateTwoChannel=BinarySymmetricChannel(90)):
        self.firstChannel = stateOneChannel
        self.secondChannel = stateTwoChannel
        self.firstToSecondPercent = 100
        self.secondToFirstPercent = 100
        self.randomizer = RandomizerImpl()
        self.inFirstState = True

    def distort(self, packet):
        if self.inFirstState:
            output = self.firstChannel.distort(packet)
        else:
            output = self.secondChannel.distort(packet)
        self.toggleState()
        return output

    def toggleState(self):
        if self.inFirstState:
            isStateChanged = self.randomizer.getTrueWithProbability(self.firstToSecondPercent)
        else:
            isStateChanged = self.randomizer.getTrueWithProbability(self.secondToFirstPercent)
        if isStateChanged:
            self.inFirstState = not self.inFirstState

    def setFirstStateChannel(self, channel):
        self.firstChannel = channel

    def setSecondStateChannel(self, channel):
        self.secondChannel = channel

    def setFirstToSecondProbabilityInPercent(self, percent):
        self.firstToSecondPercent = percent

    def setSecondToFirstProbability(self, percent):
        self.secondToFirstPercent = percent


class ChannelFactory:
    def __init__(self, channelParameters):
        self.parameters = channelParameters

    def buildChannel(self):
        return Channel


class BSCFactory(ChannelFactory):
    def buildChannel(self):
        channel = BinarySymmetricChannel(BER=self.parameters['BER'])
        return channel


class BECFactory(ChannelFactory):
    def buildChannel(self):
        channel = BinaryErasureChannel(BER=self.parameters['BER'])
        return channel


class ZChannelFactory(ChannelFactory):
    def buildChannel(self):
        channel = ZChannel(BER=self.parameters['BER'])
        return channel


class TwoStateChannelFactory(ChannelFactory):
    def buildChannel(self):
        firstChanel = AllChannelFactory.buildChannel(self.parameters['firstChannel'])
        secondChannel = AllChannelFactory.buildChannel(self.parameters['secondChannel'])
        output = TwoStateMarkovChannel(firstChanel, secondChannel)
        output.setFirstToSecondProbabilityInPercent(self.parameters['firstToSecondProbability'])
        output.setSecondToFirstProbability(self.parameters['secondToFirstProbability'])
        return output


class AllChannelFactory:
    @staticmethod
    def buildChannel(channelParameters):
        if channelParameters['type'] == Noise.BINARY_SYMMETRIC:
            factory = BSCFactory(channelParameters)
        elif channelParameters['type'] == Noise.BINARY_ERASURE:
            factory = BECFactory(channelParameters)
        elif channelParameters['type'] == Noise.Z_CHANNEL:
            factory = ZChannelFactory(channelParameters)
        elif channelParameters['type'] == Noise.TWO_STATE:
            factory = TwoStateChannelFactory(channelParameters)
        else:
            raise Exception()
        return factory.buildChannel()
