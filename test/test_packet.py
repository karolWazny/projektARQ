import unittest

from ..system.Packet import Packet


class PacketTest(unittest.TestCase):
    def test_length(self):
        packet = Packet()
        self.assertEqual(packet.length(), 0)
        packet.addBit(True)
        self.assertEqual(packet.length(), 1)
        packet.addBit(False)
        self.assertEqual(packet.length(), 2)
