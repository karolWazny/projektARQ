from system.Enums import Encoding
from system.Decoder import ParityFactory, CRCFactory, HammingFactory


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
            crc = CRCFactory(encoding['key'])
            return crc.buildEncoder()
        elif encoding['type'] == Encoding.HAMMING:
            hamming = HammingFactory(encoding)
            return hamming.buildEncoder()
        else:
            raise Exception()


class DecoderFactory:
    @staticmethod
    def createDecoder(encoding):
        decoder = DecoderFactory.chooseFabricOfDecoder(encoding)
        return decoder

    @staticmethod
    def chooseFabricOfDecoder(encoding):
        if encoding['type'] == Encoding.PARITY:
            return ParityFactory.buildDecoder()
        elif encoding['type'] == Encoding.CRC:
            crc = CRCFactory(encoding['key'])
            return crc.buildDecoder()
        elif encoding['type'] == Encoding.HAMMING:
            hamming = HammingFactory(encoding)
            return hamming.buildDecoder()
        else:
            raise Exception()
