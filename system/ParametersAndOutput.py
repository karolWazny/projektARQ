class SimulationParameters:
    def __init__(self):
        self.totalLength = None  # int
        self.packetLength = None  # int
        self.noiseModel = None  # słownik, gdzie pierwsza para identyfikuje model, pozostałe to parametry
        self.encoding = None  # słownik, gdzie pierwsza para identyfikuje model, pozostałe to parametry


class SimulationOutput:
    def __init__(self):
        self.transmissionsTotal = None
        self.retransmissions = None
        self.errorsTotal = None
        self.errorsUndetected = None
