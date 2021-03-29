class Transmitter:
    def __init__(self, packetSize, word, packet):
        self.packetSize = packetSize
        self.word = word
        self.packet = []   # zauważyłem, że tu chyba powinno byc self.packet = packet; potwierdzcie/zmiencie


def divBitString(word, packet, packetSize):
    lengthWord = (len(word))
    counter = 0
    while (counter + 1) * packetSize < lengthWord:
        packet.append(word[0 + counter * packetSize:packetSize * (counter + 1)])
        counter = counter + 1
    packet.append(word[packetSize * counter:lengthWord])
    return packet


def addBit(packet):
    packet2 = []
    for element in packet:
        counter = 0
        for bits in element:
            if bits == '1':
                counter = counter + 1
        if counter % 2 == 1:
            element = element + '1'
        else:
            element = element + '0'
        packet2.append(element)
    packet = packet2
    print(packet)
    return packet
