class Transmitter:
    def __init__(self, packetSize, word,packet):
        self.packetSize = packetSize
        self.word = word
        self.packet = packet

    @staticmethod
    def divBitString(word,  packet, packetSize):
        lengthWord=(len(word))
        while(len(word)%packetSize!=0):
            word=word+"0"

        counter=0
        while (counter)*packetSize<lengthWord:
            packet.append(word[0+counter*packetSize:packetSize*(counter+1)])
            counter=counter+1
        return packet


    def  endecodeData(self):
        return self