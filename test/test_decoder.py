import unittest
from ..system.Decoder import *
from ..system.Encoder import *


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

    def test_tripleOneHamming(self):
        builder = HammingMatrixBuilder(2)
        enc = HammingEncoder(builder)
        dec = HammingDecoder(builder)

        packet = Packet.fromList([1])

        encoded = enc.encode(packet)
        for bit in encoded.content():
            self.assertEqual(bit, 1)
        self.assertEqual(encoded.length(), 3)

        dec.passFrame(encoded)
        decoded = dec.decode()

        for bit in decoded.content():
            self.assertEqual(bit, 1)
        self.assertEqual(decoded.length(), 1)

    def test_tripleZeroHamming(self):
        builder = HammingMatrixBuilder(2)
        enc = HammingEncoder(builder)
        dec = HammingDecoder(builder)

        packet = Packet.fromList([0])

        encoded = enc.encode(packet)
        for bit in encoded.content():
            self.assertEqual(bit, 0)
        self.assertEqual(encoded.length(), 3)

        dec.passFrame(encoded)
        decoded = dec.decode()

        for bit in decoded.content():
            self.assertEqual(bit, 0)
        self.assertEqual(decoded.length(), 1)

    def test_hammingTwoParityBitsWrongPacketSize(self):
        builder = HammingMatrixBuilder(2)
        dec = HammingDecoder(builder)

        packet = Packet.fromList([1, 1])
        dec.passFrame(packet)
        try:
            dec.decode()
        except DecoderException:
            packet.length()
        else:
            self.fail()

    def test_hammingTwoParityDamagedPacketRaisesException(self):
        builder = HammingMatrixBuilder(2)
        dec = HammingDecoder(builder)

        packet = Packet.fromList([1, 1, 0])
        dec.passFrame(packet)
        try:
            dec.decode()
        except DecoderException:
            packet.length()
        else:
            self.fail()

    def test_hammingThreeParityDamagedPacketRaisesException(self):
        builder = HammingMatrixBuilder(3)
        enc = HammingEncoder(builder)
        dec = HammingDecoder(builder)

        packet = Packet.fromList([1, 1, 0, 1])

        encoded = enc.encode(packet)

        encoded.content()[5] ^= bool(1)

        dec.passFrame(encoded)
        try:
            decoded = dec.decode()
        except DecoderException:
            encoded.length()
        else:
            self.fail()






if __name__ == '__main__':
    unittest.main()
