import unittest
from ..system.Channel import Channel, BinarySymmetricChannel, BinaryErasureChannel, ZChannel
from ..system.Random import Randomizer, RandomizerImpl
from ..system.Packet import Packet


class ChannelTest(unittest.TestCase):
    def setUp(self):
        rand = RandomizerImpl()
        self.packet = Packet()
        for index in range(0, 100):
            self.packet.add(rand.getTrueWithProbability())

    def test_Channel(self):
        dist = Channel()
        self.assertEqual(self.packet, dist.distort(self.packet))

    def test_binarySymmetricChannelEveryBitIsChangedTrue(self):
        dist = BinarySymmetricChannel()
        dist.setChancesOfDistortingSingleBit(100)
        distorted = dist.distort(self.packet)
        self.assertEqual(distorted.length(), self.packet.length())
        for index in range(0, self.packet.length()):
            self.assertNotEqual(distorted.content()[index], self.packet.content()[index])

    def test_binarySymmetricChannelNoBitIsChangedFalse(self):
        dist = BinarySymmetricChannel()
        dist.setChancesOfDistortingSingleBit(0)
        distorted = dist.distort(self.packet)
        self.assertEqual(distorted.length(), self.packet.length())
        for index in range(0, self.packet.length()):
            self.assertEqual(distorted.content()[index], self.packet.content()[index])

    def test_binaryErasureChannelEveryBitIsChangedTrue(self):
        dist = BinaryErasureChannel()
        dist.setChancesOfDistortingSingleBit(100)
        distorted = dist.distort(self.packet)
        self.assertEqual(distorted.length(), 0)

    def test_binaryErasureChannelNoBitIsChangedFalse(self):
        dist = BinaryErasureChannel()
        dist.setChancesOfDistortingSingleBit(0)
        distorted = dist.distort(self.packet)
        self.assertEqual(distorted.length(), self.packet.length())
        for index in range(0, self.packet.length()):
            self.assertEqual(distorted.content()[index], self.packet.content()[index])

    def test_zChannelEveryBitIsChangedTrue(self):
        dist = ZChannel()
        dist.setChancesOfDistortingSingleBit(100)
        distorted = dist.distort(self.packet)
        self.assertEqual(distorted.length(), self.packet.length())
        for index in range(0, self.packet.length()):
            self.assertEqual(distorted.content()[index], False)

    def test_zChannelNoBitIsChangedFalse(self):
        dist = ZChannel()
        dist.setChancesOfDistortingSingleBit(0)
        distorted = dist.distort(self.packet)
        self.assertEqual(distorted.length(), self.packet.length())
        for index in range(0, self.packet.length()):
            self.assertEqual(distorted.content()[index], self.packet.content()[index])


if __name__ == '__main__':
    unittest.main()