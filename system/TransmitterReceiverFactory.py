from repo.system.Transmitter import Transmitter
from repo.system.Receiver import Receiver
from repo.system.Enums import Encoding
from repo.system.Decoder import ParityFactory, CRCFactory, HammingFactory


class TransmitterReceiverFactory:
    def __init__(self, encoding):
        self.encoderDecoderFactory = EncoderDecoderFactory(encoding)

    def createTransmitter(self):
        encoder = self.encoderDecoderFactory.createEncoder()
        return Transmitter(encoder)

    def createReceiver(self):
        decoder = self.encoderDecoderFactory.createDecoder()
        return Receiver(decoder)


class EncoderDecoderFactory:
    def __init__(self, encoding, key=None, parityBits=None):
        self.encoding = encoding
        self.key = key
        self.parityBits = parityBits

    def createEncoder(self):
        encoderFactory = self.chooseSpecificFactory(self)
        encoder = encoderFactory.buildEncoder()
        return encoder

    def createDecoder(self):
        decoderFactory = self.chooseSpecificFactory(self)
        decoder = decoderFactory.buildDecoder()
        return decoder

    def chooseSpecificFactory(self):
        if self.encoding['type'] == Encoding.PARITY:
            return ParityFactory()
        elif self.encoding['type'] == Encoding.CRC:
            return CRCFactory(self.encoding.key)
        elif self.encoding['type'] == Encoding.HAMMING:
            return HammingFactory(self.encoding.parityBits)
        else:
            raise Exception()