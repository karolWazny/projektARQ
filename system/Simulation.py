class Simulation:
    def __init__(self, signalLength, packetLength, generator, transmitter, encoder, channel, decoder, receiver, params, output):
        self.signalLength = signalLength
        self.packetLength = packetLength
        self.generator = generator
        self.transmitter = transmitter
        self.encoder = encoder
        self.channel = channel
        self.decoder = decoder
        self.receiver = receiver
        self.simulationLog = SimulationLog()
# symulacja dostanie params jako obiekt (pozmieniać) i konkretny koder/dekoder ktory bedzie stworzony w SetUp
# w setup ma być noiseModel i codingModel
    def simulate(self):
        signal = self.generator.generate(self.signalLength)
        packetList = self.transmitter.divBitString(signal, [], self.packetLength) #dzielenie sygnału na listę 8-bitowych pakietów
        codedPackets = self.encoder.encode(packetList)
        decodedPackets = []
        n = 0
        while n < len(packetList):
            output.transmissionsTotal += 1
            distortedPacket = self.channel.distort(codedPackets[n])
            receivedPacket = self.receiver.decodeData(distortedPacket)
            self.decoder.passFrame(receivedPacket)
            decodedPacket = self.decoder.decode()
            if packetList[n] != decodedPacket:
                output.retransmissions += 1  # simulationLog - zapis ze retransmisja się odbyła (zwiększ licznik retransmisji)
            else:
                decodedPackets.append(decodedPacket)
                n += 1
# sprawdzic pakiet przed zakodowaniem i odebrany (po zdekodowaniu) czy sa takie same == niewykryte bledy
        if len(packetList) != len(decodedPackets):
            output.errorsUndetected = abs(len(packetList) - len(decodedPackets))

        self.simulationLog.params = parameter
        self.simulationLog.output = output
        return self.simulationLog


