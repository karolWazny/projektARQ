from .Generator import *
from .Packet import *
# tu powinien być koder
from .Transmitter import *
from .Distortion import *
# tu powinien być odbiornik
from .Decoder import *
# tu powinno być sprawdzenie poprawności(?)
#powyższe importy prawdopodobnie zostaną użyte w Fabryce Obiektów ale zapisałem je sobie tutaj dla jasności
#choć możliwe, że wygodniej będzie tworzyć obiekty tutaj

class Simulation:
    def simulationInterface(self):
        return simulationObject

    def __init__(self, signalLength, packetLength, generator, transmitter, distortion, decoder):
        self.signalLength = signalLength
        self.packetLength = packetLength
        self.generator = generator
        self.transmitter = transmitter
        self.distortion = distortion
        self.decoder = decoder

    def simulation(self):
        signal = self.generator.generate(self.signalLength)
        packetList = self.transmitter.divBitString(signal, 1, self.packetLength)
        codedPackets = self.transmitter.addBit(packetList)
        for x in codedPackets:
            distortedPacket = self.distortion.distort(x)
            decoder.passFrame(distortedPacket)
            decodedPacket = decoder.decode()
            #sprawdzenie poprawnosci z wygenerowanym pakietem i zapis jesli uleglo znieksztalceniu