import unittest
from ..system.Encoder import *

class ParityEncoderTest(unittest.TestCase):
    def test_encode(self):
        results=ParityEncoder.encode(self, ['0100', '1110', '0101','0110'])
        self.assertTrue(results==['01001', '11101', '01010','01100'])

if __name__ == '__main__':
    unittest.main()
