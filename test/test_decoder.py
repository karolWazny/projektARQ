import unittest
from ..system.Decoder import *


class DecoderTest(unittest.TestCase):
    def test_evenDecoderEmptyPacketThrowsException(self):
        packet = Packet()
        decoder = EvenDecoder()
        decoder.passFrame(packet)
        try:
            decoder.decode()
        except DecoderException:
            pass
        else:
            self.fail(msg="Pusty pakiet powinien wywołać błąd dekodera")

if __name__ == '__main__':
    unittest.main()
