from .Generator import *
from .Transmitter import *  # coder
from .Distortion import *
from .Decoder import *
from .Receiver import *

class AbstractFactory:
    def produceObjects(self):
        generator = Generator()
        transmitter = Transmitter()
        distortion = Distortion()
        decoder = Decoder()
        receiver = Receiver()
<<<<<<< HEAD
        return generator, transmitter, distortion, decoder, receiver
=======
        return generator, transmitter, distortion, decoder, receiver
>>>>>>> origin/master
