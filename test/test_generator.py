import unittest

from ..system.Generator import Generator


class GeneratorTest(unittest.TestCase):
    def test_generatingLength(self):
        generator = Generator()
        signal = generator.generate(2)
        self.assertEqual(len(signal), 2)
