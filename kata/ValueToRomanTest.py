import unittest
import ValueToRoman


class RomanNumeralFromValueTest(unittest.TestCase):
    def test_one(self):
        self.assertEqual("I", ValueToRoman.romanNumeralFromValue(1))

    def test_two(self):
        self.assertEqual("II", ValueToRoman.romanNumeralFromValue(2))

    def test_three(self):
        self.assertEqual("III", ValueToRoman.romanNumeralFromValue(3))

    def test_ten(self):
        self.assertEqual("X", ValueToRoman.romanNumeralFromValue(10))
if __name__ == '__main__':
    unittest.main()
