import unittest

from system.Packet import Packet
from system.Transmitter import Transmitter


class TransmitterTestDiv(unittest.TestCase):
    def test_divSignal1(self):
        results1 = Transmitter.divSignal([1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],  5)
        self.assertEqual([Packet.fromList([1, 0, 1, 1, 0]), Packet.fromList([1, 1, 1, 1, 0]), Packet.fromList([1, 0, 0, 0, 0])], results1)

    def test_divSignal2(self):
        results1 = Transmitter.divSignal([1, 0, 0, 1, 0, 1, 0, 1, 0, 1], 5)
        self.assertEqual([Packet.fromList([1, 0, 0, 1, 0]), Packet.fromList([1, 0, 1, 0, 1])], results1)

if __name__ == '__main__':
    unittest.main()
