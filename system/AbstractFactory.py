from .Generator import *
from .Transmitter import *  # coder
from .Channel import *
from .Decoder import *
from .Receiver import *
from .Encoder import *

class AbstractFactory:
    def produceObjects(self):
        generator = Generator()
        transmitter = Transmitter()
        distortion = Channel()
        decoder = Decoder()
        encoder = Encoder()
        receiver = Receiver()
        return generator, transmitter, distortion, decoder, encoder, receiver
