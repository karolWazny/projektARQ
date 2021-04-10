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
        packet.add(True)
        packet.add(True)
        packet.add(False)
        packet.add(False)
        decoder.passFrame(packet)
        decoded = None
        try:
            decoded = decoder.decode()
        except DecoderException:
            self.fail(msg="Prawidłowy pakiet nie powinien rzucać wyjątku")

    def test_evenDecoderIncorrectPacketThrows(self):
        packet = Packet()
        decoder = EvenDecoder()
        packet.add(True)
        packet.add(True)
        packet.add(True)
        packet.add(False)
        decoder.passFrame(packet)
        decoded = None
        try:
            decoded = decoder.decode()
        except DecoderException:
            pass
        else:
            self.fail(msg="Nieprawidłowy pakiet powinien rzucać wyjątek.")

    def test_evenDecoderDecodesPackage(self):
        packet = Packet()
        decoder = EvenDecoder()
        packet.add(True)
        packet.add(True)
        packet.add(True)
        packet.add(False)
        packet.add(True)
        decoder.passFrame(packet)
        decoded = None
        decodedReference = Packet()
        decodedReference.add(True)
        decodedReference.add(True)
        decodedReference.add(True)
        decodedReference.add(False)
        try:
            decoded = decoder.decode()
        except DecoderException:
            self.fail(msg="Prawidłowy pakiet nie powinien rzucać wyjątku")
        else:
            self.assertEqual(decoded.length(), decodedReference.length())
            self.assertEqual(decoded.content(), decodedReference.content())

    def test_hammingMatrixMultipliedGiveZero(self):
        for index in range(2, 11):
            self.checkHammingForMEqual(index)

    def checkHammingForMEqual(self, m):
        builder = HammingMatrixBuilder(m)
        h = builder.buildHMatrix()
        g = builder.buildGMatrix().transpose()
        matrix = h.dot(g)
        for row in matrix:
            for value in row:
                value &= 0x1
                self.assertEqual(value, 0)


if __name__ == '__main__':
    unittest.main()
