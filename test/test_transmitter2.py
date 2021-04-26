import unittest
from ..system.Transmitter2 import Transmitter


class TransmitterTestDiv(unittest.TestCase):
    def test_divSignal1(self):
        results1 = Transmitter.divSignal([1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],  5)
        self.assertTrue(results1 == [[1, 0, 0, 1, 0], [1, 0, 1, 0, 1], [0, 0, 0, 0, 0]])

    def test_divSignal2(self):
        results1 = Transmitter.divSignal(self, [1, 0, 0, 1, 0, 1, 0, 1, 0, 1], 5)
        self.assertTrue(results1 == [[1, 0, 0, 1, 0], [1, 0, 1, 0, 1]])


if __name__ == '__main__':
    unittest.main()
