import unittest
from ..system.Receiver import *

class ReceiverTest(unittest.TestCase):
    def test_decodeData(self):
        receiver = Receiver()
        self.assertEqual(True)

if __name__ == '__main__':
    unittest.main()
