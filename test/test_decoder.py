import unittest
from ..system.Decoder import *


class DecoderTest(unittest.TestCase):
    def test_evenDecoderEmptyPacketThrowsException(self):
        packet = Packet()
        decoder = EvenDecoder()
        decoder.passFrame(packet)
        try:
            decoder.decode()
        except DecoderException:
            pass
        else:
            self.fail(msg="Pusty pakiet powinien wywołać błąd dekodera")

    def test_evenDecoderCorrectPacketNoThrow(self):
        packet = Packet()
        decoder = EvenDecoder()
        packet.addBit(True)
        packet.addBit(True)
        packet.addBit(False)
        packet.addBit(False)
        decoder.passFrame(packet)
        decoded = None
        try:
            decoded = decoder.decode()
        except DecoderException:
            self.fail(msg="Prawidłowy pakiet nie powinien rzucać wyjątku")

    def test_evenDecoderIncorrectPacketThrows(self):
        packet = Packet()
        decoder = EvenDecoder()
        packet.addBit(True)
        packet.addBit(True)
        packet.addBit(True)
        packet.addBit(False)
        decoder.passFrame(packet)
        decoded = None
        try:
            decoded = decoder.decode()
        except DecoderException:
            pass
        else:
            self.fail(msg="Nieprawidłowy pakiet powinien rzucać wyjątek.")


if __name__ == '__main__':
    unittest.main()
