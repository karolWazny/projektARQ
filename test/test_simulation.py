import unittest

from ..system.Simulation import Simulation
from ..system.Enums import *
from ..system.Generator import Generator


class SimulationTest(unittest.TestCase):
    def test_generating(self):
        simulation = Simulation(259, 8, Noise.BINARY_SYMMETRIC, Encoding.PARITY, Generator(), ) #podać atrybuty testowe

        #przetestować czy dane wejściowe zgadzają się z simulationLog.parameter na wyjściu

