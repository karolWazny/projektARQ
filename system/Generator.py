import random


class Generator:
    def generate(self, length):
        signal = []
        for x in range(length):
            signal.append(random.randint(0, 1))
        return signal
