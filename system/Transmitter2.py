class Transmitter2:
    def __init__(self, encoder):
        self.encoder = encoder

    def transmit(self, packet):
        return self.encoder.encode(packet)
