class Packet:
    def __init__(self):
        self.packet = []

    def add(self, bit):
        self.packet.append(bit)

    def length(self):
        return len(self.packet)

    def read(self):
        return self.packet
