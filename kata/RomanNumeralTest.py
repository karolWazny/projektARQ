import unittest
import RomanNumeral


class RomanNumeralFromValueTest(unittest.TestCase):
    def test_one(self):
        self.assertEqual("I", RomanNumeral.fromValue(1))

    def test_two(self):
        self.assertEqual("II", RomanNumeral.fromValue(2))

    def test_three(self):
        self.assertEqual("III", RomanNumeral.fromValue(3))

    def test_ten(self):
        self.assertEqual("X", RomanNumeral.fromValue(10))

    def test_twenty(self):
        self.assertEqual("XX", RomanNumeral.fromValue(20))

    def test_thirty(self):
        self.assertEqual("XXX", RomanNumeral.fromValue(30))

    def test_hundred(self):
        self.assertEqual("C", RomanNumeral.fromValue(100))

    def test_two_hundred(self):
        self.assertEqual("CC", RomanNumeral.fromValue(200))

    def test_hundred_one(self):
        self.assertEqual("CI", RomanNumeral.fromValue(101))

    def test_thousand(self):
        self.assertEqual("M", RomanNumeral.fromValue(1000))

    def test_five(self):
        self.assertEqual("V", RomanNumeral.fromValue(5))
if __name__ == '__main__':
    unittest.main()
