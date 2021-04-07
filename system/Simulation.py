class Simulation:
    def __init__(self, signalLength, packetLength, generator, transmitter, distortion, decoder, receiver):
        self.signalLength = signalLength
        self.packetLength = packetLength
        self.generator = generator
        self.transmitter = transmitter
        self.distortion = distortion
        self.decoder = decoder
        self.receiver = receiver

    def simulate(self):
        signal = self.generator.generate(self.signalLength)
        packetList = self.transmitter.divBitString(signal, 1, self.packetLength) #dzielenie sygnału na listę 8-bitowych pakietów
        codedPackets = self.transmitter.addBit(packetList)
        for x in codedPackets:
            distortedPacket = self.distortion.distort(x)
            self.decoder.passFrame(distortedPacket)
            decodedPacket = self.decoder.decode() #nie rozumiem w pełni decodera
            receivedData = self.receiver #tu też nie do końca wiem jak to użyć
            return  #musimy uzgodnić co zwracamy
