import unittest
from ..system.Distortion import Distortion, SimpleDistortion
from ..system.Random import Randomizer, RandomizerImpl
from ..system.Packet import Packet


class DistortionTest(unittest.TestCase):
    def setUp(self):
        rand = RandomizerImpl()
        self.packet = Packet()
        for index in range(0, 100):
            self.packet.add(rand.getTrueWithProbability())

    def test_DefaultDistortion(self):
        dist = Distortion()
        self.assertEqual(self.packet, dist.distort(self.packet))

    def test_simpleDistortionEveryBitIsChangedTrue(self):
        dist = SimpleDistortion()
        dist.setChancesOfDistortingSingleBit(100)
        distorted = dist.distort(self.packet)
        self.assertEqual(distorted.length(), self.packet.length())
        for index in range(0, self.packet.length()):
            self.assertNotEqual(distorted.content()[index], self.packet.content()[index])

    def test_simpleDistortionNoBitIsChangedFalse(self):
        dist = SimpleDistortion()
        dist.setChancesOfDistortingSingleBit(0)
        distorted = dist.distort(self.packet)
        self.assertEqual(distorted.length(), self.packet.length())
        for index in range(0, self.packet.length()):
            self.assertEqual(distorted.content()[index], self.packet.content()[index])


if __name__ == '__main__':
    unittest.main()