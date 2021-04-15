class Simulation:
    def __init__(self, signalLength, packetLength, noiseModel, codingModel, generator, transmitter, channel, decoder, receiver):
        self.signalLength = signalLength
        self.packetLength = packetLength
        self.generator = generator
        self.transmitter = transmitter
        self.channel = channel
        self.decoder = decoder
        self.receiver = receiver
        self.noiseModel = noiseModel
        self.codingModel = codingModel

    def simulate(self):
        signal = self.generator.generate(self.signalLength)
        packetList = self.transmitter.divBitString(signal, 1, self.packetLength) #dzielenie sygnału na listę 8-bitowych pakietów
        codedPackets = self.transmitter.addBit(packetList)
        n = 0
        while n < len(packetList):
            distortedPacket = self.channel.distort(codedPackets[n])
            receivedPacket = self.receiver.decodeData(distortedPacket)
            self.decoder.passFrame(receivedPacket)
            decodedPacket = self.decoder.decode()
            if packetList[n] != decodedPacket:
                pass
                # simulationLog - zapisz ze retransmisja się odbyła (zwiększ licznik retransmisji)
            else:
                n += 1
        return  #musimy uzgodnić co zwracamy (liczba transmisji, liczba retransmisji, pakiety uszkodzone(?) )


