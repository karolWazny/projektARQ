from .Transmitter import Transmitter
from .Receiver import Receiver
from .DecoderEncoderFactory import DecoderFactory, EncoderFactory


class TransmitterFactory:
    @staticmethod
    def createTransmitter(encoding):
        encoder = EncoderFactory.createEncoder(encoding)
        return Transmitter(encoder)


class ReceiverFactory:
    @staticmethod
    def createReceiver(encoding, params):
        decoder = DecoderFactory.createDecoder(encoding, params)
        return Receiver(decoder)
