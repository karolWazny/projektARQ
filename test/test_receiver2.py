import unittest
from ..system.Receiver2 import Receiver
from ..system.Decoder import Decoder, ParityDecoder
from ..system.Packet import Packet


class ReceiverTest(unittest.TestCase):
    def test_receive(self):
        receiver = Receiver(ParityDecoder())
        packet = Packet()
        receivedPacket = receiver.receive(packet)
        print(receivedPacket)
        self.assertEqual(None, receivedPacket)


if __name__ == '__main__':
    unittest.main()
