from .Decoder import DecoderException


class Receiver:
    def __init__(self, decoder):
        self.decoder = decoder

    def receive(self, packet):
        try:
            self.decoder.passFrame(packet)
            return self.decoder.decode()
        except DecoderException:
            return None



