import random
from Encoder import div

class Generator:
    def __init__(self, length):
        self.length = length

    def generate(self):
        signal = []
        for x in range(self.length):
            signal.append(random.randint(0, 1))
        return signal
