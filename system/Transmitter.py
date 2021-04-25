from Encoder import*
class Transmitter:
    def __init__(self, packetSize, signal,packetList):
        self = None
        self.packetSize = packetSize
        self.signal = signal
        self.packetList = packetList

    def divSignal(self, signal, packetList, packetSize):
        key = []
        packetList=[[0] * 0 for i in range(0)]
        packet = []
        counter = 0
        for x in signal:
            packet.append(x)
            counter += 1
            if(counter == packetSize):
                packetList.append(packet)
                Encoder.encode(self, packet)
                ParityEncoder.encode(self,packet)
                CRCEncoder.encode(self,packet,key)
                HammingEncoder.encode(self,packet)
                packet = []
                counter = 0
        if(counter!=0):
            packetList.append(packet)
            Encoder.encode(self, packet)
            ParityEncoder.encode(self,packet)
            CRCEncoder.encode(self,packet,key)
            HammingEncoder.encode(self,packet)
        return packetList

