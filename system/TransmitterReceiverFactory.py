from repo.system.Transmitter import Transmitter
from repo.system.Receiver import Receiver
from repo.system.DecoderEncoderFactory import DecoderFactory, EncoderFactory


class TransmitterFactory:
    @staticmethod
    def createTransmitter(encoding):
        encoder = EncoderFactory.createEncoder(encoding)
        return Transmitter(encoder)


class ReceiverFactory:
    @staticmethod
    def createReceiver(encoding):
        decoder = DecoderFactory.createDecoder(encoding)
        return Receiver(decoder)
