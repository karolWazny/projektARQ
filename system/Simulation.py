from .ParametersAndOutput import *


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
        self.simulationLog = SimulationLog()

    def simulate(self):
        parameter = SimulationParameters()
        parameter.packetLength = self.packetLength
        parameter.noiseModel = self.noiseModel
        parameter.totalLength = self.signalLength
        parameter.encoding = self.codingModel

        output = SimulationOutput()
        output.transmissionsTotal = 0
        output.retransmissions = 0
        output.errorsTotal = 0

        signal = self.generator.generate(self.signalLength)
        packetList = self.transmitter.divBitString(signal, [], self.packetLength) #dzielenie sygnału na listę 8-bitowych pakietów
        codedPackets = self.transmitter.addBit(packetList)
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

        if len(packetList) != len(decodedPackets):
            output.errorsUndetected = abs(len(packetList) - len(decodedPackets))

        self.simulationLog.params = parameter
        self.simulationLog.output = output
        return self.simulationLog


