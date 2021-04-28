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
    def __init__(self, encoding):
        self.encoding = encoding

    def createEncoder(self):
        encoderFactory = self.chooseSpecificFactory()
        encoder = encoderFactory.buildEncoder()
        return encoder

    def createDecoder(self):
        decoderFactory = self.chooseSpecificFactory()
        decoder = decoderFactory.buildDecoder()
        return decoder

    def chooseSpecificFactory(self):
        if self.encoding['type'] == Encoding.PARITY:
            return ParityFactory()
        elif self.encoding['type'] == Encoding.CRC:
            return CRCFactory(self.encoding['key'])
        elif self.encoding['type'] == Encoding.HAMMING:
            return HammingFactory(self.encoding['parityBits'])
        else:
            raise Exception()
