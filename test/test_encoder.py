import unittest
from system.Encoder import *
from system.Decoder import *


class ParityEncoderTest(unittest.TestCase):
    def test_encode1(self):
        results = ParityEncoder().encode(Packet.fromList([1, 0]))
        self.assertTrue(results == [1, 0, 1])

    def test_encode2(self):
        results = ParityEncoder().encode(Packet.fromList([1, 0, 1, 0]))
        self.assertTrue(results == [1, 0, 1, 0, 0])

    def test_encodeDecode(self):
        initialPacket = Packet.fromList([0, 1, 0, 1, 0, 1, 0])
        encodedPacket = ParityEncoder().encode(initialPacket)
        decoder = ParityDecoder()
        decoder.passFrame(encodedPacket)
        decodedPacket = decoder.decode()
        self.assertEqual(initialPacket, decodedPacket)


class CRCEncoderTest(unittest.TestCase):
    def test_encode1(self):
        results = CRCEncoder([1, 0, 1, 1]).encode(Packet.fromList([1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1]))
        self.assertTrue(results == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])

    def test_encode2(self):
        results = CRCEncoder([1, 0, 1, 1]).encode(Packet.fromList([1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0]))
        self.assertTrue(results == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])


if __name__ == '__main__':
    unittest.main()
