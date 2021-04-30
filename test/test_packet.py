import unittest

from system.Packet import Packet


class PacketTest(unittest.TestCase):
    def test_length(self):
        packet = Packet()
        self.assertEqual(packet.length(), 0)
        packet.add(True)
        self.assertEqual(packet.length(), 1)
        packet.add(False)
        self.assertEqual(packet.length(), 2)

    def test_clear(self):
        packet = Packet()
        packet.add(4)
        self.assertEqual(packet.length(), 1)
        packet.clear()
        self.assertEqual(packet.length(), 0)


if __name__ == '__main__':
    unittest.main()
