from repo.system.Transmitter import Transmitter
from repo.system.Receiver2 import Receiver
from repo.system.DecoderEncoderFactory import DecoderFactory, EncoderFactory


class TransmitterFactory:
    @staticmethod
    def createTransmitter(encoding, crcKey, parityBits):
        encoder = EncoderFactory.createEncoder(encoding, crcKey, parityBits)
        return Transmitter(encoder)


class ReceiverFactory:
    @staticmethod
    def createReceiver(encoding, crcKey, parityBits):
        decoder = DecoderFactory.createDecoder(encoding, crcKey, parityBits)
        return Receiver(decoder)
