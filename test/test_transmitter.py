import unittest
import Transmitter
from projekty.system.Transmitter import divBitString
from projekty.system.Transmitter import addBit

class TransmitterTestDiv(unittest.TestCase):
    def test_divBitString(self):
       results1=divBitString("010011100101011",[], 4)
       self.assertTrue(results1==['0100', '1110', '0101','011'])
class TransmitterTestAdd(unittest.TestCase):
    def test_AddBit(self):
        results2=addBit(['0100', '1110', '0101','011'])
        self.assertTrue(results2==['01001', '11101', '01010','0110'])

if __name__ == '__main__':
    unittest.main()