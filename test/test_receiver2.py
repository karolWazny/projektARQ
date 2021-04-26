import unittest
from ..system.Receiver2 import Receiver
from ..system.Decoder import Decoder


class ReceiverTest(unittest.TestCase):
    def receive(self):
        receiver = Receiver(Decoder)
        receivedPacket = receiver.receive()
        print(receivedPacket)
        self.assertIsNone(receivedPacket)


if __name__ == '__main__':
    unittest.main()
