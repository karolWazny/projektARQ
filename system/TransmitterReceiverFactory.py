from .Transmitter import Transmitter
from .Receiver2 import Receiver
from .DecoderEncoderFactory import DecoderFactory, EncoderFactory


class TransmitterFactory:
    @staticmethod
    def createTransmitter(encoding, params):
        encoder = EncoderFactory.createEncoder(encoding, params)
        return Transmitter(encoder)


class ReceiverFactory:
    @staticmethod
    def createReceiver(encoding, params):
        decoder = DecoderFactory.createDecoder(encoding, params)
        return Receiver(decoder)
