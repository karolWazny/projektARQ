from repo.system.Enums import Encoding
from repo.system.Decoder import ParityFactory, CRCFactory, HammingFactory


class EncoderFactory:
    @staticmethod
    def createEncoder(encoding, key=None, parityBits=None):
        encoder = EncoderFactory.chooseFabricOfEncoder(encoding, key, parityBits)
        return encoder

    @staticmethod
    def chooseFabricOfEncoder(encoding, key, parityBits):
        if encoding['type'] == Encoding.PARITY:
            return ParityFactory.buildEncoder()
        elif encoding['type'] == Encoding.CRC:
            crc = CRCFactory(key)
            return crc.buildEncoder()
        elif encoding['type'] == Encoding.HAMMING:
            hamming = HammingFactory(encoding)
            return hamming.buildEncoder()
        else:
            raise Exception()


class DecoderFactory:
    @staticmethod
    def createDecoder(encoding, key=None, parityBits=None):
        decoder = DecoderFactory.chooseFabricOfDecoder(encoding, key, parityBits)
        return decoder

    @staticmethod
    def chooseFabricOfDecoder(encoding, key, parityBits):
        if encoding['type'] == Encoding.PARITY:
            return ParityFactory.buildDecoder()
        elif encoding['type'] == Encoding.CRC:
            crc = CRCFactory(key)
            return crc.buildDecoder()
        elif encoding['type'] == Encoding.HAMMING:
            hamming = HammingFactory(encoding)
            return hamming.buildDecoder()
        else:
            raise Exception()
