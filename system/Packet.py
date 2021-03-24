class Packet:
    def __init__(self):
        self.__packet = []

    def add(self, bit):
        self.__packet.append(bit)

    def length(self):
        return len(self.__packet)

    def content(self):
        return self.__packet
