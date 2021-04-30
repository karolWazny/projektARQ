from system.Enums import *
import unittest


class EnumTest(unittest.TestCase):
    def test_enumEqualsEnum(self):
        parity = Encoding.PARITY
        hamming = Encoding.HAMMING
        hamming2 = Encoding.HAMMING
        self.assertTrue(hamming == hamming2)
        self.assertFalse(hamming != hamming2)
        self.assertTrue(hamming != parity)
        self.assertFalse(hamming == parity)

    def test_enumEqualsString(self):
        parityEnum = Encoding.PARITY
        parityString = 'PARITY'
        hammingString = 'HAMMING'
        self.assertTrue(parityEnum == parityString)
        self.assertTrue(parityString == parityEnum)
        self.assertFalse(parityString != parityEnum)
        self.assertFalse(parityEnum != parityString)
        self.assertTrue(parityEnum != hammingString)
        self.assertTrue(hammingString != parityEnum)
        self.assertFalse(hammingString == parityEnum)
        self.assertFalse(parityEnum == hammingString)
