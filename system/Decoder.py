from .Packet import Packet


class Decoder:
    def __init__(self):
        self.currentFrame = None

    def passFrame(self, packet):
        self.currentFrame = packet

    def decode(self):
        return self.currentFrame


class EvenDecoder(Decoder):
    def decode(self):
        if self.currentFrame.length() == 0:
            raise DecoderException
        isOdd = False
        output = Packet()
        for bit in self.currentFrame.read():
            isOdd = bool(isOdd) ^ bool(bit)
        if isOdd:
            raise DecoderException
        return self.currentFrame


class DecoderException(Exception):
    """Wyjątek zgłaszany jako informacja o błędzie wykrytym w
    dekodowanym pakiecie."""

    def doSmth(self):
        return
