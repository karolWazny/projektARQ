import unittest
from ..system.Encoder import *


class ParityEncoderTest(unittest.TestCase):
    def test_encode1(self):
        results = ParityEncoder.encode(self, [1,0])
        self.assertTrue(results == [1,0,1])
    def test_encode2(self):
        results = ParityEncoder.encode(self, [1,0,1,0])
        self.assertTrue(results == [1,0,1,0,0])

class CRCEncoderTest(unittest.TestCase):
    def test_encode1(self):
        results = CRCEncoder.encode(self,[1,1,0,1,0,0,1,1,1,0,1,1,1,0,0,1,0,1,1,1],[1,0,1,1])
        self.assertTrue(results == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
    def test_encode2(self):
        results = CRCEncoder.encode(self,[1,1,0,1,0,0,1,1,1,0,1,1,0,0],[1,0,1,1])
        self.assertTrue(results == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])

if __name__ == '__main__':
    unittest.main()
