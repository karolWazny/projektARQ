class Simulation:
    def __init__(self, generator, channel, transmitter, receiver, simulationLog):
        self.generator = generator
        self.channel = channel
        self.transmitter = transmitter
        self.receiver = receiver
        self.simulationLog = simulationLog

    def simulate(self):
        signal = self.generator.generate()
        packetList = self.transmitter.divBitString(signal, [], self.simulationLog.params.packetLength)  # dzielenie sygnału na listę pakietów
#        codedPackets = self.encoder.encode(packetList)
        receivedPackets = []
        while len(packetList) != len(receivedPackets):
            for packet in packetList:
                try:
                    self.simulationLog.output.transmissionsTotal += 1
                    codedPacket = self.transmitter(packet)
                    distortedPacket = self.channel.distort(codedPacket)
                    receivedPacket = self.receiver.decodeData(distortedPacket)
                    if packet != receivedPacket:
                        self.simulationLog.output.retransmissions += 1
                    else:
                        receivedPackets.append(receivedPacket)
                except:
                    pass

        # sprawdzic pakiet przed zakodowaniem i odebrany (po zdekodowaniu) czy sa takie same == niewykryte bledy

        return self.simulationLog
