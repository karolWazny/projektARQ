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
        return self.currentFrame


class DecoderException(Exception):
    def doSmth(self):
        return
