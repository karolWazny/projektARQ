import unittest

from ..system.Generator import Generator


class GeneratorTest(unittest.TestCase):
    def test_generating(self):
        generator = Generator()
        signal = generator.generate(10)
        self.assertEqual(len(signal), 10)