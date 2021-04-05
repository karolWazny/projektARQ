import unittest
from ..system.Transmitter import *

class TransmitterTestDiv(unittest.TestCase):
    def test_divBitString(self):
       results1=Transmitter.divBitString("010011100101011",[], 4)
       self.assertTrue(results1==['0100', '1110', '0101','0110'])

class TransmitterTestAdd(unittest.TestCase):
    def test_AddBit(self):
        results2=Transmitter.addBit(['0100', '1110', '0101','0110'])
        self.assertTrue(results2==['01001', '11101', '01010','01100'])

if __name__ == '__main__':
    unittest.main()