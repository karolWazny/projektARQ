import unittest
from ..system.Transmitter import *

class TransmitterTestDiv(unittest.TestCase):
    def test_divBitString(self):
       results1=Transmitter.divBitString("010011100101011",[], 4)
       self.assertTrue(results1==['0100', '1110', '0101','0110'])

if __name__ == '__main__':
    unittest.main()