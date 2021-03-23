import random


class Randomizer:
    def getBooleanWithProbability(self, percent=50):
        return True


class RandomizerImpl(Randomizer):
    def getBooleanWithProbability(self, percent=50):
        return percent >= random.randint(a=1, b=100)
