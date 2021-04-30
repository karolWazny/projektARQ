import unittest

from system.Generator import Generator


class GeneratorTest(unittest.TestCase):
    def test_generating(self):
        generator = Generator(10)
        signal = generator.generate()
        self.assertEqual(len(signal), 10)
